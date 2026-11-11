
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Challenge
from app.schemas import ChallengeCreate, ChallengeOut

router = APIRouter(
    prefix="/challenges",
    tags=["Workout Challenges"]
)


@router.post("/", response_model=ChallengeOut)
def create_challenge(
    data: ChallengeCreate,
    db: Session = Depends(get_db)
):
    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    challenge = Challenge(**data.model_dump())

    db.add(challenge)
    db.commit()
    db.refresh(challenge)

    return challenge


@router.get("/", response_model=list[ChallengeOut])
def get_challenges(db: Session = Depends(get_db)):
    return db.query(Challenge).all()


@router.get("/{challenge_id}", response_model=ChallengeOut)
def get_challenge(
    challenge_id: int,
    db: Session = Depends(get_db)
):
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id
    ).first()

    if not challenge:
        raise HTTPException(
            status_code=404,
            detail="Challenge not found"
        )

    return challenge


@router.delete("/{challenge_id}")
def delete_challenge(
    challenge_id: int,
    db: Session = Depends(get_db)
):
    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id
    ).first()

    if not challenge:
        raise HTTPException(
            status_code=404,
            detail="Challenge not found"
        )

    db.delete(challenge)
    db.commit()

    return {"message": "Challenge deleted successfully"}

@router.put("/{challenge_id}")
def update_challenge(
    challenge_id: int,
    data: ChallengeCreate,
    db: Session = Depends(get_db)
):
    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=400,
            detail="End date must be after start date"
        )

    challenge = db.query(Challenge).filter(
        Challenge.id == challenge_id
    ).first()

    if not challenge:
        raise HTTPException(
            status_code=404,
            detail="Challenge not found"
        )

    challenge.title = data.title
    challenge.description = data.description
    challenge.target_workouts = data.target_workouts
    challenge.duration_days = data.duration_days
    challenge.start_date = data.start_date
    challenge.end_date = data.end_date

    db.commit()
    db.refresh(challenge)

    return challenge