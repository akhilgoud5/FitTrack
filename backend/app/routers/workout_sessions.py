
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, WorkoutSession

router = APIRouter(
    prefix="/workout-sessions",
    tags=["Workout Timer & Live Tracking"]
)


# START WORKOUT
@router.post("/start")
def start_workout(
    workout_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    active = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == current_user.id,
        WorkoutSession.status.in_(["ONGOING", "PAUSED"])
    ).first()

    if active:
        raise HTTPException(
            status_code=400,
            detail="You already have an active workout session"
        )

    session = WorkoutSession(
        user_id=current_user.id,
        workout_name=workout_name,
        start_time=datetime.utcnow(),
        status="ONGOING"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "message": "Workout started successfully",
        "session_id": session.id,
        "status": session.status
    }


# PAUSE WORKOUT
@router.put("/pause/{session_id}")
def pause_workout(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.id == session_id,
        WorkoutSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != "ONGOING":
        raise HTTPException(status_code=400, detail="Workout is not ongoing")

    session.paused_at = datetime.utcnow()
    session.status = "PAUSED"

    db.commit()

    return {
        "message": "Workout paused successfully",
        "session_id": session.id,
        "status": session.status
    }


# RESUME WORKOUT
@router.put("/resume/{session_id}")
def resume_workout(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.id == session_id,
        WorkoutSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != "PAUSED" or session.paused_at is None:
        raise HTTPException(status_code=400, detail="Workout is not paused")

    paused_seconds = int(
        (datetime.utcnow() - session.paused_at).total_seconds()
    )

    session.total_paused_seconds += paused_seconds
    session.paused_at = None
    session.status = "ONGOING"

    db.commit()

    return {
        "message": "Workout resumed successfully",
        "session_id": session.id,
        "status": session.status
    }


# STOP WORKOUT
@router.put("/stop/{session_id}")
def stop_workout(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.id == session_id,
        WorkoutSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status not in ["ONGOING", "PAUSED"]:
        raise HTTPException(status_code=400, detail="Workout already completed")

    now = datetime.utcnow()

    if session.status == "PAUSED" and session.paused_at:
        session.total_paused_seconds += int(
            (now - session.paused_at).total_seconds()
        )
        session.paused_at = None

    elapsed_seconds = (now - session.start_time).total_seconds()
    actual_seconds = max(0, elapsed_seconds - session.total_paused_seconds)

    session.end_time = now
    session.duration_minutes = round(actual_seconds / 60)
    # Estimate calories burned using 62 kg body weight
    duration_hours = actual_seconds / 3600

# Approximate moderate workout intensity (5 METs)
    session.calories_burned = round(
    5 * 3.5 * 62 / 200 * duration_hours,
    2
    )
    session.status = "COMPLETED"

    db.commit()
    db.refresh(session)

    return {
    "message": "Workout completed successfully",
    "session_id": session.id,
    "duration_minutes": session.duration_minutes,
    "calories_burned": session.calories_burned,
    "status": session.status
}


# ACTIVE WORKOUT
@router.get("/active")
def get_active_workout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(WorkoutSession).filter(
        WorkoutSession.user_id == current_user.id,
        WorkoutSession.status.in_(["ONGOING", "PAUSED"])
    ).first()

    if not session:
        return {"message": "No active workout session"}

    return session


# WORKOUT HISTORY
@router.get("/")
def get_workout_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(WorkoutSession).filter(
        WorkoutSession.user_id == current_user.id
    ).order_by(WorkoutSession.start_time.desc()).all()
