from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.services import subscription_service

router = APIRouter()

@router.post("/create-checkout/{plan}")
async def create_checkout(
    plan: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if plan not in ["basic", "pro", "enterprise"]:
        raise HTTPException(status_code=400, detail="Invalid plan selected")
    
    checkout_url = subscription_service.create_lemonsqueezy_checkout(plan, current_user.email)
    return {"checkout_url": checkout_url}

@router.post("/webhook")
async def lemonsqueezy_webhook(event_name: str, data: dict, db: Session = Depends(get_db)):
    subscription_service.handle_lemonsqueezy_webhook(db, event_name, data)
    return {"status": "success"}