
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Subscription, UserSubscription, User
from app.schemas import (
    SubscriptionCreate,
    SubscriptionOut,
    UserSubscriptionOut
)
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscription Plans"]
)


# Create Subscription Plan
@router.post("/", response_model=SubscriptionOut, status_code=201)
def create_subscription(
    plan_data: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Subscription).filter(
        Subscription.name == plan_data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Subscription plan already exists"
        )

    new_plan = Subscription(
        name=plan_data.name,
        price=plan_data.price,
        duration=plan_data.duration,
        features=plan_data.features
    )

    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)

    return new_plan


# View All Subscription Plans
@router.get("/", response_model=list[SubscriptionOut])
def get_subscriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Subscription).all()


# View Subscription Details
@router.get("/{subscription_id}", response_model=SubscriptionOut)
def get_subscription(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )

    return plan


# Subscribe / Upgrade / Downgrade
@router.post(
    "/{subscription_id}/subscribe",
    response_model=UserSubscriptionOut,
    status_code=201
)
def subscribe_to_plan(
    subscription_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not plan:
        raise HTTPException(
            status_code=404,
            detail="Subscription plan not found"
        )

    now = datetime.now(timezone.utc)

    # End the user's previous active subscription
    previous = db.query(UserSubscription).filter(
        UserSubscription.user_id == current_user.id,
        UserSubscription.end_date > now
    ).all()

    for old_subscription in previous:
        old_subscription.end_date = now

    # Create new subscription
    new_subscription = UserSubscription(
        user_id=current_user.id,
        subscription_id=plan.id,
        start_date=now,
        end_date=now + timedelta(days=plan.duration)
    )

    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    return new_subscription


# View Current User Subscription
@router.get("/me/current", response_model=UserSubscriptionOut)
def get_my_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    now = datetime.now(timezone.utc)

    subscription = db.query(UserSubscription).filter(
        UserSubscription.user_id == current_user.id,
        UserSubscription.end_date > now
    ).order_by(
        UserSubscription.start_date.desc()
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="No active subscription found"
        )

    return subscription
