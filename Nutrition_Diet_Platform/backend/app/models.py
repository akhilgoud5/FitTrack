
from sqlalchemy import ( Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean)
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, index=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

from sqlalchemy import ForeignKey, Text


# Diet Plans Table
class DietPlan(Base):
    __tablename__ = "diet_plans"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)

    description = Column(Text, nullable=True)

    goal_type = Column(String(50), nullable=False)

    daily_calories = Column(Integer, nullable=False)

    duration = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


# User Diet Plan Assignment Table
class UserDietPlan(Base):
    __tablename__ = "user_diet_plans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    diet_plan_id = Column(
        Integer,
        ForeignKey("diet_plans.id"),
        nullable=False
    )

    assigned_at = Column(DateTime(timezone=True), server_default=func.now())

# Meals Table
class Meal(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    meal_type = Column(String(50), nullable=False)

    food_name = Column(String(150), nullable=False)

    calories = Column(Float, nullable=False)

    protein = Column(Float, default=0.0)

    carbs = Column(Float, default=0.0)

    fats = Column(Float, default=0.0)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

# Subscription Plans Table
class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), unique=True, nullable=False)

    price = Column(Float, nullable=False)

    duration = Column(Integer, nullable=False)

    features = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# User Subscriptions Table
class UserSubscription(Base):
    __tablename__ = "user_subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    subscription_id = Column(
        Integer,
        ForeignKey("subscriptions.id"),
        nullable=False
    )

    start_date = Column(DateTime(timezone=True), nullable=False)

    end_date = Column(DateTime(timezone=True), nullable=False)


# Nutritionists Table
class Nutritionist(Base):
    __tablename__ = "nutritionists"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    specialization = Column(String(150), nullable=False)

    experience = Column(Integer, nullable=False)

    contact_info = Column(String(255), nullable=False)


# Consultations Table
class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    nutritionist_id = Column(
        Integer,
        ForeignKey("nutritionists.id"),
        nullable=False
    )

    scheduled_time = Column(DateTime(timezone=True), nullable=False)

    status = Column(String(50), default="PENDING")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# Notifications Table
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String(150), nullable=False)

    message = Column(Text, nullable=False)

    is_read = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# Module 8: Doctor Support & Appointment Management

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    experience = Column(Integer, default=0)
    contact_info = Column(String(150))
    availability_status = Column(String(30), default="AVAILABLE")
    created_at = Column(DateTime, server_default=func.now())


class DoctorAppointment(Base):
    __tablename__ = "doctor_appointments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    time_slot = Column(String(50), nullable=False)
    status = Column(String(30), default="PENDING")
    created_at = Column(DateTime, server_default=func.now())
