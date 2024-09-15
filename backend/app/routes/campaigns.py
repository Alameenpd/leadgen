from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.campaign import Campaign, CampaignCreate, CampaignWithLeads
from app.services import campaign_service
from app.tasks.campaign_tasks import send_campaign_dms


router = APIRouter()

@router.post("/", response_model=Campaign)
def create_campaign(
    campaign: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return campaign_service.create_campaign(db=db, campaign=campaign, user_id=current_user.id)

@router.get("/", response_model=List[Campaign])
def read_campaigns(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return campaign_service.get_campaigns(db=db, user_id=current_user.id)

@router.get("/{campaign_id}", response_model=CampaignWithLeads)
def read_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    campaign = campaign_service.get_campaign(db=db, campaign_id=campaign_id, user_id=current_user.id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.put("/{campaign_id}", response_model=Campaign)
def update_campaign(
    campaign_id: int,
    campaign: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    updated_campaign = campaign_service.update_campaign(db=db, campaign_id=campaign_id, campaign=campaign, user_id=current_user.id)
    if updated_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return updated_campaign

@router.delete("/{campaign_id}", response_model=Campaign)
def delete_campaign(
    campaign_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    deleted_campaign = campaign_service.delete_campaign(db=db, campaign_id=campaign_id, user_id=current_user.id)
    if deleted_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return deleted_campaign

@router.post("/{campaign_id}/leads", response_model=CampaignWithLeads)
def add_leads_to_campaign(
    campaign_id: int,
    lead_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    updated_campaign = campaign_service.add_leads_to_campaign(db=db, campaign_id=campaign_id, lead_ids=lead_ids, user_id=current_user.id)
    if updated_campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return updated_campaign

@router.post("/{campaign_id}/start")
def start_campaign(
    campaign_id: int,
    email: str,
    password: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    campaign = campaign_service.get_campaign(db, campaign_id, current_user.id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    background_tasks.add_task(send_campaign_dms.delay, campaign_id, email, password)
    return {"message": f"Campaign {campaign_id} started"}