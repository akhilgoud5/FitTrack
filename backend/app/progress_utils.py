
from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import Workout, Progress


def sync_daily_progress(
    db: Session,
    user_id: int,
    workout_date: date
):
    # Calculate total workouts for the selected date
    total_workouts = db.query(Workout).filter(
        Workout.user_id == user_id,
        Workout.workout_date == workout_date
    ).count()

    # Calculate total calories for the selected date
    total_calories = db.query(
        func.coalesce(
            func.sum(Workout.calories_burned), 0
        )
    ).filter(
        Workout.user_id == user_id,
        Workout.workout_date == workout_date
    ).scalar()

    # Find existing daily progress
    progress = db.query(Progress).filter(
        Progress.user_id == user_id,
        Progress.date == workout_date
    ).first()

    try:
        # Delete progress if no workouts exist
        if total_workouts == 0:
            if progress:
                db.delete(progress)

        # Update existing progress
        elif progress:
            progress.total_workouts = total_workouts
            progress.total_calories = total_calories

        # Create new progress
        else:
            progress = Progress(
                user_id=user_id,
                total_workouts=total_workouts,
                total_calories=total_calories,
                date=workout_date
            )
            db.add(progress)

        db.commit()

        if progress and total_workouts > 0:
            db.refresh(progress)

    except Exception:
        db.rollback()
        raise
