from fastapi import FastAPI

from .database import Base, engine
from .routes import router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="CareCloud Voice AI Patient Registration API",
    description="REST API for patient registration and management.",
    version="1.0.0"
)


# Register patient routes
app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "CareCloud Voice AI Patient Registration API is running",
        "status": "ok"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }