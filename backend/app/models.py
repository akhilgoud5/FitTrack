
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    ForeignKey,
    Boolean,
    UniqueConstraint,
    func
)
from sqlalchemy.orm import relationship

from app.database import Base


# 1. USER MODEL
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    workouts = relationship("Workout", back_populates="user")


# 2. WORKOUT MODEL
class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    workout_name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    duration = Column(Integer, nullable=False)
    calories_burned = Column(Integer, nullable=False)
    workout_date = Column(Date, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="workouts")


# 3. PROGRESS MODEL
class Progress(Base):
    __tablename__ = "progress"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "date",
            name="unique_user_daily_progress"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    total_workouts = Column(Integer, default=0, nullable=False)
    total_calories = Column(Integer, default=0, nullable=False)

    date = Column(Date, nullable=False)


# 4. GOAL MODEL
class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    goal_type = Column(String(50), nullable=False)
    target_value = Column(Integer, nullable=False)
    current_value = Column(Integer, default=0)

    deadline = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


# 5. NOTIFICATION MODEL
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    message = Column(String(255), nullable=False)
    is_read = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())
