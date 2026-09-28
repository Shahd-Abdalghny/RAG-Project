from fastapi import FastAPI , APIRouter ,Depends
from helpers.config import get_settings ,Settings

# Base router for general application-level endpoints.
base_router = APIRouter(
    prefix = "/api/v1",
    tags = ["api_v1"],
)

# Root endpoint returns basic app information loaded from environment settings.
@base_router.get("/")
async def welcome_message(app_settings : Settings = Depends(get_settings)):
    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    return {
        "app_name": app_name,
        "app_version": app_version,
        }