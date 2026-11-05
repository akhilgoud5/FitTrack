
from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Badge, Workout, User
from app.schemas import BadgeOut
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/badges",
    tags=["Achievement Badges"]
)

BADGE_MILESTONES = [
    (1, "First Workout", "Completed your first workout."),
    (5, "Getting Started", "Completed 5 workouts."),
    (10, "Fitness Enthusiast", "Completed 10 workouts."),
    (25, "Fitness Champion", "Completed 25 workouts."),
    (50, "Fitness Legend", "Completed 50 workouts.")
]


def award_workout_badges(db: Session, user_id: int):
    total_workouts = db.query(Workout).filter(
        Workout.user_id == user_id
    ).count()

    for count, name, description in BADGE_MILESTONES:
        if total_workouts >= count:
            existing = db.query(Badge).filter(
                Badge.user_id == user_id,
                Badge.badge_name == name
            ).first()

            if existing is None:
                db.add(Badge(
                    user_id=user_id,
                    badge_name=name,
                    description=description,
                    earned_at=datetime.utcnow()
                ))

    # Do not commit here.
    # The calling workout route handles the transaction.


@router.post("/evaluate", response_model=list[BadgeOut])
def evaluate_badges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        award_workout_badges(db, current_user.id)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return db.query(Badge).filter(
        Badge.user_id == current_user.id
    ).order_by(Badge.earned_at.desc()).all()


@router.get("/me", response_model=list[BadgeOut])
def get_my_badges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Badge).filter(
        Badge.user_id == current_user.id
    ).order_by(Badge.earned_at.desc()).all()
