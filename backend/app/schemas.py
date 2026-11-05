from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Literal


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

class ProgressOut(BaseModel):
    id: int
    user_id: int
    total_workouts: int
    total_calories: int
    date: date

    model_config = ConfigDict(from_attributes=True)


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

class NotificationOut(BaseModel):
    id: int
    user_id: int
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# 7. WORKOUT PLAN SCHEMAS

class WorkoutPlanCreate(BaseModel):

    title: str = Field(min_length=2, max_length=150)

    description: str | None = Field(
        default=None,
        max_length=500
    )

    scheduled_date: date


class WorkoutPlanUpdate(BaseModel):

    title: str = Field(min_length=2, max_length=150)

    description: str | None = Field(
        default=None,
        max_length=500
    )

    scheduled_date: date


class WorkoutPlanOut(BaseModel):

    id: int
    user_id: int
    title: str
    description: str | None = None
    scheduled_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)   


# 8. EXERCISE SCHEMAS

class ExerciseCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=150
    )

    category: Literal["Cardio", "Strength", "Yoga"]

    description: str | None = Field(
        default=None,
        max_length=500
    )

    duration: int = Field(
        gt=0,
        le=1440
    )


class ExerciseOut(BaseModel):

    id: int
    name: str
    category: str
    description: str | None = None
    duration: int

    model_config = ConfigDict(from_attributes=True)

class BadgeOut(BaseModel):
    id: int
    user_id: int
    badge_name: str
    description: str
    earned_at: datetime

    model_config = ConfigDict(from_attributes=True)
