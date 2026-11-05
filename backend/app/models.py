
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
    func,
    Table
)
from sqlalchemy.orm import relationship

from app.database import Base


# WORKOUT-EXERCISE ASSOCIATION TABLE
workout_exercises = Table(
    "workout_exercises",
    Base.metadata,
    Column(
        "workout_id",
        Integer,
        ForeignKey("workouts.id"),
        primary_key=True
    ),
    Column(
        "exercise_id",
        Integer,
        ForeignKey("exercises.id"),
        primary_key=True
    )
)


# 1. USER MODEL
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(
        String(80),
        unique=True,
        index=True,
        nullable=False
    )
    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    workouts = relationship("Workout", back_populates="user")
    workout_plans = relationship("WorkoutPlan", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    progress_records = relationship("Progress", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

    streak = relationship(
        "Streak",
        back_populates="user",
        uselist=False
    )

    badges = relationship(
        "Badge",
        back_populates="user"
    )


# 2. WORKOUT MODEL
class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    workout_name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    duration = Column(Integer, nullable=False)
    calories_burned = Column(Integer, nullable=False)
    workout_date = Column(Date, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = relationship("User", back_populates="workouts")

    exercises = relationship(
        "Exercise",
        secondary=workout_exercises,
        back_populates="workouts"
    )


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
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    total_workouts = Column(Integer, default=0, nullable=False)
    total_calories = Column(Integer, default=0, nullable=False)

    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="progress_records")


# 4. GOAL MODEL
class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    goal_type = Column(String(50), nullable=False)
    target_value = Column(Integer, nullable=False)
    current_value = Column(Integer, default=0, nullable=False)

    deadline = Column(Date, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = relationship("User", back_populates="goals")


# 5. NOTIFICATION MODEL
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    message = Column(String(255), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    user = relationship("User", back_populates="notifications")


# 6. WORKOUT PLAN MODEL
class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    scheduled_date = Column(Date, nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = relationship("User", back_populates="workout_plans")


# 7. EXERCISE MODEL
class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(String(500), nullable=True)
    duration = Column(Integer, nullable=False)

    workouts = relationship(
        "Workout",
        secondary=workout_exercises,
        back_populates="exercises"
    )


# 8. STREAK MODEL
class Streak(Base):
    __tablename__ = "streaks"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    last_workout_date = Column(Date, nullable=True)

    user = relationship("User", back_populates="streak")


# 9. ACHIEVEMENT BADGE MODEL
class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    badge_name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)

    earned_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "badge_name",
            name="unique_user_badge"
        ),
    )

    user = relationship("User", back_populates="badges")
