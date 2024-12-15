"""
main.py
--------

This module is the entry point of the application,
responsible for setting up and starting the FastAPI app.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.database import db_models
from api.database.database import engine
from api.routes.pharmacy_route import router as pharmacy_router
from api.routes.mask_route import router as mask_router
from api.routes.user_route import router as user_router
from api.routes.transaction_route import router as transaction_router
from api.utils.tools import install_pg_trgm, generate_openapi_json

# Create database tables if they do not exist
db_models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Handle startup and shutdown events for the FastAPI app.
    """
    install_pg_trgm(engine)
    generate_openapi_json(_app)
    yield


# Initialize the FastAPI app with custom lifespan events
app = FastAPI(lifespan=lifespan)

# Include routers for the API endpoints
app.include_router(pharmacy_router)
app.include_router(mask_router)
app.include_router(user_router)
app.include_router(transaction_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
