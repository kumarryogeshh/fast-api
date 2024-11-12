"""
Pytest configuration file.
Contains fixtures and configuration for tests.
"""

import asyncio
import pytest
from typing import Generator, AsyncGenerator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from fastapi.testclient import TestClient
from app.core.database import Base
from app.main import app
from app.api.deps import get_db

# Synchronous database for regular tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async database for async tests
ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
)

AsyncTestingSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_db():
    """Create test database fixtures."""
    Base.metadata.create_all(bind=engine)
    yield  # Run the tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db) -> Generator:
    """
    Create a fresh database session for each test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session  # Run the test

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
async def async_db_session() -> AsyncGenerator:
    """
    Create a fresh async database session for each test.
    """
    async with async_engine.connect() as conn:
        await conn.begin()
        async_session = AsyncTestingSessionLocal(bind=conn)

        yield async_session  # Run the test

        await async_session.close()
        await conn.rollback()


@pytest.fixture(scope="function")
def client(db_session: TestingSessionLocal) -> Generator:  # type: ignore
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()
