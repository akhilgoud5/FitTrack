
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import User
from app.schemas import RegisterIn, LoginIn, UserOut, TokenOut
from app.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# 1. USER REGISTRATION
@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED
)
def register(
    data: RegisterIn,
    db: Session = Depends(get_db)
):
    username = data.username.strip()
    email = str(data.email).strip().lower()

    existing = db.query(User).filter(
        or_(
            User.email == email,
            User.username == username
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or username already registered"
        )

    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(data.password)
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to register user"
        )

    return user


# 2. USER LOGIN
@router.post("/login", response_model=TokenOut)
def login(
    data: LoginIn,
    db: Session = Depends(get_db)
):
    email = str(data.email).strip().lower()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None or not verify_password(
        data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = create_access_token(
        subject=str(user.id)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# 3. GET LOGGED-IN USER PROFILE
@router.get("/me", response_model=UserOut)
def read_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user
