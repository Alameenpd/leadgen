from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.services import analytics_service

router = APIRouter()

@router.get("/overall")
def get_overall_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return analytics_service.get_overall_stats(db, current_user.id)

@router.get("/daily")
def get_daily_stats(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return analytics_service.get_daily_stats(db, current_user.id, days)

@router.get("/campaign/{campaign_id}")
def get_campaign_analytics(
    campaign_id: int,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=30)
    if not end_date:
        end_date = datetime.utcnow()
    
    return analytics_service.get_campaign_analytics(db, campaign_id, start_date, end_date)