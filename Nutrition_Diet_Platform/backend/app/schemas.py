
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# User Registration Schema
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


# User Login Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# User Response Schema
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


# JWT Token Response Schema
class Token(BaseModel):
    access_token: str
    token_type: str


from typing import Literal


# Create Diet Plan Schema
class DietPlanCreate(BaseModel):
    title: str
    description: str
    goal_type: Literal["Weight Loss", "Muscle Gain", "Maintenance"]
    daily_calories: int = Field(gt=0)
    duration: int = Field(gt=0)


# Diet Plan Response Schema
class DietPlanOut(BaseModel):
    id: int
    title: str
    description: str | None
    goal_type: str
    daily_calories: int
    duration: int
    created_at: datetime

    model_config = {"from_attributes": True}


# User Diet Plan Assignment Schema
class UserDietPlanCreate(BaseModel):
    diet_plan_id: int = Field(gt=0)


# User Diet Plan Assignment Response
class UserDietPlanOut(BaseModel):
    id: int
    user_id: int
    diet_plan_id: int
    assigned_at: datetime

    model_config = {"from_attributes": True}

# Meal Creation Schema
class MealCreate(BaseModel):
    meal_type: Literal["Breakfast", "Lunch", "Dinner", "Snacks"]

    food_name: str = Field(min_length=2, max_length=150)

    calories: float = Field(ge=0)

    protein: float = Field(default=0.0, ge=0)

    carbs: float = Field(default=0.0, ge=0)

    fats: float = Field(default=0.0, ge=0)


# Meal Response Schema
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

    model_config = {"from_attributes": True}


# Daily Nutrition Summary Schema
class NutritionSummary(BaseModel):
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float
    total_meals: int

# Subscription Plan Creation Schema
class SubscriptionCreate(BaseModel):
    name: Literal["Free", "Premium", "Pro"]

    price: float = Field(ge=0)

    duration: int = Field(gt=0)

    features: str


# Subscription Plan Response Schema
class SubscriptionOut(BaseModel):
    id: int
    name: str
    price: float
    duration: int
    features: str
    created_at: datetime

    model_config = {"from_attributes": True}


# User Subscription Purchase Schema
class UserSubscriptionCreate(BaseModel):
    subscription_id: int = Field(gt=0)


# User Subscription Response Schema
class UserSubscriptionOut(BaseModel):
    id: int
    user_id: int
    subscription_id: int
    start_date: datetime
    end_date: datetime

    model_config = {"from_attributes": True}


# Nutritionist Creation Schema
class NutritionistCreate(BaseModel):
    name: str = Field(min_length=3, max_length=150)

    specialization: str

    experience: int = Field(ge=0)

    contact_info: str


# Nutritionist Response Schema
class NutritionistOut(BaseModel):
    id: int
    name: str
    specialization: str
    experience: int
    contact_info: str

    model_config = {"from_attributes": True}


# Consultation Booking Schema
class ConsultationCreate(BaseModel):
    nutritionist_id: int = Field(gt=0)

    scheduled_time: datetime


# Consultation Response Schema
class ConsultationOut(BaseModel):
    id: int
    user_id: int
    nutritionist_id: int
    scheduled_time: datetime
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


# Diet Recommendation Request
class DietRecommendationRequest(BaseModel):
    goal_type: Literal["Weight Loss", "Muscle Gain", "Maintenance"]

    calories_requirement: int = Field(gt=0)

    activity_level: Literal[
        "Sedentary",
        "Light",
        "Moderate",
        "Active",
        "Very Active"
    ]


# Diet Recommendation Response
class DietRecommendationOut(BaseModel):
    goal_type: str
    calories_requirement: int
    activity_level: str
    recommended_plans: list[DietPlanOut]


# Notification Creation Schema
class NotificationCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)

    message: str = Field(min_length=3)


# Notification Response Schema
class NotificationOut(BaseModel):
    id: int
    user_id: int
    title: str
    message: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# Module 8: Doctor Support & Appointment Management

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    experience: int = 0
    contact_info: str | None = None
    availability_status: str = "AVAILABLE"


class DoctorOut(BaseModel):
    id: int
    name: str
    specialization: str
    experience: int
    contact_info: str | None = None
    availability_status: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True


class DoctorAppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: datetime
    time_slot: str


class DoctorAppointmentOut(BaseModel):
    id: int
    user_id: int
    doctor_id: int
    appointment_date: datetime
    time_slot: str
    status: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True
