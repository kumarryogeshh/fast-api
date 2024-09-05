from fastapi import FastAPI
from core.config import settings
from apis.app_router import router


def initialize_router(app):
    """
    Initialize the FastAPI application with the main router.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    app.include_router(router=router)


def start_application():
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    initialize_router(app=app)
    return app


app = start_application()
