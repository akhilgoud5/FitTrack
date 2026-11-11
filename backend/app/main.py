
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models

from app.routers import (auth, workouts,progress,goals,reports,notifications)
from app.routers import workout_plans
from app.routers import exercises
from app.routers import dashboard
from app.routers import badges
from app.routers import meals
from app.routers import water
from app.routers import recommendations
from app.routers import workout_sessions
from app.routers import integrations
from app.routers import exports
from app.routers import analytics
from app.routers import reminders
from app.routers import challenges

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables during application startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="FitTrack API",
    version="1.0.0",
    lifespan=lifespan
)


# CORS CONFIGURATION
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# REGISTER ROUTERS
app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(progress.router)
app.include_router(goals.router)
app.include_router(reports.router)
app.include_router(notifications.router)
app.include_router(workout_plans.router)
app.include_router(exercises.router)
app.include_router(dashboard.router)
app.include_router(badges.router)
app.include_router(meals.router)
app.include_router(water.router)
app.include_router(recommendations.router)
app.include_router(workout_sessions.router)
app.include_router(integrations.router)
app.include_router(exports.router)
app.include_router(analytics.router)
app.include_router(reminders.router)
app.include_router(challenges.router)

# ROOT ENDPOINT
@app.get("/")
def home():
    return {
        "message": "Welcome to FitTrack API"
    }


# HEALTH CHECK ENDPOINT
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "FitTrack API is running"
    }
