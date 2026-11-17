
from fastapi import FastAPI

from app import models
from app.database import engine

from app.routers import (
    auth,
    diet_plans,
    meals,
    subscriptions,
    nutritionists,
    recommendations,
    notifications,
    doctors
)

# Create FastAPI application
app = FastAPI(
    title="Nutrition & Diet Management Platform",
    description="Backend API for nutrition and diet management",
    version="1.0.0"
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Register API routers
app.include_router(auth.router)
app.include_router(diet_plans.router)
app.include_router(meals.router)
app.include_router(subscriptions.router)
app.include_router(nutritionists.router)
app.include_router(recommendations.router)
app.include_router(notifications.router)
app.include_router(doctors.router)

# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to Nutrition & Diet Management Platform API",
        "status": "Running"
    }
