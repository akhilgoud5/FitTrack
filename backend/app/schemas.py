
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# 1. AUTHENTICATION SCHEMAS

class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# 2. WORKOUT SCHEMAS

class WorkoutCreate(BaseModel):
    workout_name: str = Field(min_length=2, max_length=150)
    category: Literal["Cardio", "Strength", "Yoga"]
    duration: int = Field(gt=0, le=1440)
    calories_burned: int = Field(ge=0)
    workout_date: date


class WorkoutUpdate(BaseModel):
    workout_name: str = Field(min_length=2, max_length=150)
    category: Literal["Cardio", "Strength", "Yoga"]
    duration: int = Field(gt=0, le=1440)
    calories_burned: int = Field(ge=0)
    workout_date: date


class WorkoutOut(BaseModel):
    id: int
    user_id: int
    workout_name: str
    category: str
    duration: int
    calories_burned: int
    workout_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# 3. PROGRESS SCHEMAS

class ProgressOut(BaseModel):
    id: int
    user_id: int
    total_workouts: int
    total_calories: int
    date: date

    model_config = ConfigDict(from_attributes=True)


# 4. GOAL SCHEMAS

class GoalCreate(BaseModel):
    goal_type: Literal["Weight Loss", "Muscle Gain", "Steps"]
    target_value: int = Field(gt=0)
    current_value: int = Field(default=0, ge=0)
    deadline: date


class GoalUpdate(BaseModel):
    goal_type: Literal["Weight Loss", "Muscle Gain", "Steps"]
    target_value: int = Field(gt=0)
    current_value: int = Field(ge=0)
    deadline: date


class GoalOut(BaseModel):
    id: int
    user_id: int
    goal_type: str
    target_value: int
    current_value: int
    deadline: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# 5. NOTIFICATION SCHEMAS

class NotificationOut(BaseModel):
    id: int
    user_id: int
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# 6. WORKOUT PLAN SCHEMAS

class WorkoutPlanCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    scheduled_date: date


class WorkoutPlanUpdate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str | None = Field(default=None, max_length=500)
    scheduled_date: date


class WorkoutPlanOut(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None = None
    scheduled_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# 7. EXERCISE SCHEMAS

class ExerciseCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    category: Literal["Cardio", "Strength", "Yoga"]
    description: str | None = Field(default=None, max_length=500)
    duration: int = Field(gt=0, le=1440)


class ExerciseOut(BaseModel):
    id: int
    name: str
    category: str
    description: str | None = None
    duration: int

    model_config = ConfigDict(from_attributes=True)


# 8. BADGE SCHEMAS

class BadgeOut(BaseModel):
    id: int
    user_id: int
    badge_name: str
    description: str
    earned_at: datetime

    model_config = ConfigDict(from_attributes=True)


# 9. NUTRITION & MEAL TRACKING SCHEMAS

class MealCreate(BaseModel):
    meal_type: Literal["Breakfast", "Lunch", "Dinner", "Snacks"]
    food_name: str = Field(min_length=2, max_length=150)
    calories: float = Field(ge=0)
    protein: float = Field(default=0.0, ge=0)
    carbs: float = Field(default=0.0, ge=0)
    fats: float = Field(default=0.0, ge=0)


class MealOut(BaseModel):
    id: int
    user_id: int
    meal_type: str
    food_name: str
    calories: float
    protein: float
    carbs: float
    fats: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NutritionSummary(BaseModel):
    date: date
    total_meals: int
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float


# 10. WATER INTAKE SCHEMAS

class WaterIntakeCreate(BaseModel):
    amount_ml: int = Field(gt=0, le=5000)


class WaterIntakeOut(BaseModel):
    id: int
    user_id: int
    amount_ml: int
    logged_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WaterIntakeSummary(BaseModel):
    date: date
    total_water_ml: int
    daily_goal_ml: int
    remaining_ml: int


# 11. WORKOUT REMINDER SCHEMAS

class ReminderCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    message: str | None = Field(default=None, max_length=255)
    reminder_type: Literal["WORKOUT", "MEAL", "WATER"] = "WORKOUT"
    remind_at: datetime


class ReminderUpdate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    message: str | None = Field(default=None, max_length=255)
    reminder_type: Literal["WORKOUT", "MEAL", "WATER"] = "WORKOUT"
    remind_at: datetime
    is_completed: bool = False


class ReminderOut(BaseModel):
    id: int
    user_id: int
    title: str
    message: str | None
    reminder_type: str
    remind_at: datetime
    is_completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# 12. CHALLENGE SCHEMAS

class ChallengeCreate(BaseModel):
    title: str
    description: str | None = None
    target_workouts: int = 10
    duration_days: int = 30
    start_date: date
    end_date: date


class ChallengeOut(BaseModel):
    id: int
    title: str
    description: str | None
    target_workouts: int
    duration_days: int
    start_date: date
    end_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
