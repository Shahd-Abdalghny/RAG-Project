from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import base ,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import Settings
# Create the FastAPI application instance.


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    settings = Settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URI)
    app.mongo_db = app.mongo_conn[settings.MONGODB_DB_NAME]

    yield

    # Shutdown
    app.mongo_conn.close()

app = FastAPI(lifespan=lifespan)
# Register the API routers so the endpoints are exposed.
app.include_router(base.base_router)
app.include_router(data.data_router)

