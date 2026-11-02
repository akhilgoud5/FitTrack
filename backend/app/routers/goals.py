
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Goal, User
from app.schemas import GoalCreate, GoalUpdate, GoalOut
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/goals",
    tags=["Goals"]
)


# 1. CREATE GOAL
@router.post(
    "/",
    response_model=GoalOut,
    status_code=status.HTTP_201_CREATED
)
def create_goal(
    data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.deadline < date.today():
        raise HTTPException(
            status_code=400,
            detail="Deadline cannot be in the past"
        )

    if data.current_value > data.target_value:
        raise HTTPException(
            status_code=400,
            detail="Current value cannot exceed target value"
        )

    goal = Goal(
        user_id=current_user.id,
        goal_type=data.goal_type,
        target_value=data.target_value,
        current_value=data.current_value,
        deadline=data.deadline
    )

    try:
        db.add(goal)
        db.commit()
        db.refresh(goal)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to create goal"
        )

    return goal


# 2. GET ALL MY GOALS
@router.get("/", response_model=list[GoalOut])
def get_my_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Goal).filter(
        Goal.user_id == current_user.id
    ).order_by(Goal.created_at.desc()).all()


# 3. GET GOAL BY ID
@router.get("/{goal_id}", response_model=GoalOut)
def get_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    return goal


# 4. UPDATE GOAL
@router.put("/{goal_id}", response_model=GoalOut)
def update_goal(
    goal_id: int,
    data: GoalUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    if data.deadline < date.today():
        raise HTTPException(
            status_code=400,
            detail="Deadline cannot be in the past"
        )

    if data.current_value > data.target_value:
        raise HTTPException(
            status_code=400,
            detail="Current value cannot exceed target value"
        )

    goal.goal_type = data.goal_type
    goal.target_value = data.target_value
    goal.current_value = data.current_value
    goal.deadline = data.deadline

    try:
        db.commit()
        db.refresh(goal)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to update goal"
        )

    return goal


# 5. DELETE GOAL
@router.delete("/{goal_id}")
def delete_goal(
    goal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()

    if goal is None:
        raise HTTPException(
            status_code=404,
            detail="Goal not found"
        )

    try:
        db.delete(goal)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to delete goal"
        )

    return {
        "message": "Goal deleted successfully"
    }
