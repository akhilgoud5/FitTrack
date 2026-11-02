
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Notification, User
from app.dependencies import get_current_user
from app.schemas import NotificationOut
from fastapi import Query
from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


# 1. CREATE NOTIFICATION
@router.post("/", response_model=NotificationOut, status_code=201)
def create_notification(
    
    message: str = Query(..., min_length=1, max_length=255),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = Notification(
        user_id=current_user.id,
        message=message
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


# 2. GET ALL NOTIFICATIONS
@router.get("/", response_model=list[NotificationOut])
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).all()


# 3. GET UNREAD NOTIFICATIONS
@router.get("/unread", response_model=list[NotificationOut])
def get_unread_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read.is_(False)
    ).order_by(Notification.created_at.desc()).all()


# 4. MARK NOTIFICATION AS READ
@router.put("/{notification_id}/read", response_model=NotificationOut)
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification


# 5. DELETE NOTIFICATION
@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    db.delete(notification)
    db.commit()

    return {
        "message": "Notification deleted successfully"
    }
