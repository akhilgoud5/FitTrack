from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, Reminder
from app.schemas import (
    ReminderCreate,
    ReminderUpdate,
    ReminderOut
)

router = APIRouter(
    prefix="/reminders",
    tags=["Workout Reminders"]
)

# 1. CREATE REMINDER
@router.post("/", response_model=ReminderOut, status_code=201)
def create_reminder(
    data: ReminderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reminder = Reminder(
        user_id=current_user.id,
        title=data.title,
        message=data.message,
        reminder_type=data.reminder_type,
        remind_at=data.remind_at
    )

    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    return reminder


# 2. GET ALL REMINDERS
@router.get("/", response_model=list[ReminderOut])
def get_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Reminder).filter(
        Reminder.user_id == current_user.id
    ).order_by(Reminder.remind_at.asc()).all()


# 3. GET UPCOMING REMINDERS
@router.get("/upcoming", response_model=list[ReminderOut])
def get_upcoming_reminders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Reminder).filter(
        Reminder.user_id == current_user.id,
        Reminder.remind_at >= datetime.utcnow(),
        Reminder.is_completed.is_(False)
    ).order_by(Reminder.remind_at.asc()).all()


# 4. UPDATE REMINDER
@router.put("/{reminder_id}", response_model=ReminderOut)
def update_reminder(
    reminder_id: int,
    data: ReminderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if reminder is None:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    reminder.title = data.title
    reminder.message = data.message
    reminder.reminder_type = data.reminder_type
    reminder.remind_at = data.remind_at
    reminder.is_completed = data.is_completed

    db.commit()
    db.refresh(reminder)

    return reminder


# 5. MARK REMINDER AS COMPLETED
@router.put("/{reminder_id}/complete", response_model=ReminderOut)
def complete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if reminder is None:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    reminder.is_completed = True

    db.commit()
    db.refresh(reminder)

    return reminder


# 6. DELETE REMINDER
@router.delete("/{reminder_id}")
def delete_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reminder = db.query(Reminder).filter(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    ).first()

    if reminder is None:
        raise HTTPException(
            status_code=404,
            detail="Reminder not found"
        )

    db.delete(reminder)
    db.commit()

    return {
        "message": "Reminder deleted successfully"
    }
