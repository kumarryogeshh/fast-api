from fastapi import FastAPI
from core.config import settings
from apis.app_router import router


def initialize_router(app):
    app.include_router(router=router)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    initialize_router(app=app)
    return app


app = start_application()
