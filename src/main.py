from fastapi import FastAPI
from routes import base ,data

# Create the FastAPI application instance.
app = FastAPI()

# Register the API routers so the endpoints are exposed.
app.include_router(base.base_router)
app.include_router(data.data_router)

