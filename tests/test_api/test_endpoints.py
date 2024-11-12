"""
Test module for API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_tables(client: TestClient, db_session: Session):
    """Test retrieving database tables."""
    response = client.get("/api/v1/tables")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert data["success"] is True
    assert "data" in data
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_async_db_session(async_db_session):
    """Test async database session."""
    async with async_db_session as session:
        result = await session.execute("SELECT 1")
        assert result is not None


def test_invalid_table(client: TestClient):
    """Test accessing an invalid table."""
    response = client.get("/api/v1/tables/nonexistent_table/records")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
