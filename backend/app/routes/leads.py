from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies.auth import get_current_active_user
from app.models.user import User
from app.schemas.lead import Lead, LeadCreate, LeadUpdate
from app.services import lead_service
from app.services.lead_scraper_service import lead_scraper
router = APIRouter()

class LinkedInScrapingRequest:
    search_query: str
    max_results: int = 10
    email: str | None = None
    password: str | None = None
    cookies: List[Dict] | None = None
    proxies: List[str] | None = None

@router.get("/", response_model=List[Lead])
def read_leads(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    leads = lead_service.get_leads(db, skip=skip, limit=limit, user_id=current_user.id)
    return leads

@router.post("/", response_model=Lead)
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    return lead_service.create_lead(db=db, lead=lead, user_id=current_user.id)

@router.get("/{lead_id}", response_model=Lead)
def read_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_lead = lead_service.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    if db_lead.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this lead")
    return db_lead

@router.put("/{lead_id}", response_model=Lead)
def update_lead(
    lead_id: int,
    lead: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_lead = lead_service.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    if db_lead.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this lead")
    return lead_service.update_lead(db=db, lead_id=lead_id, lead=lead)

@router.delete("/{lead_id}", response_model=Lead)
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_lead = lead_service.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    if db_lead.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this lead")
    return lead_service.delete_lead(db=db, lead_id=lead_id)

@router.post("/scrape-twitter", response_model=List[Lead])
async def scrape_twitter_leads(
    search_query: str,
    max_results: int = 10,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    async def scrape_and_save():
        scraped_leads = await lead_scraper.scrape_twitter(search_query, max_results)
        for lead in scraped_leads:
            lead_service.create_lead(db=db, lead=lead, user_id=current_user.id)

    background_tasks.add_task(scrape_and_save)
    return {"message": f"Scraping {max_results} leads from Twitter for query: {search_query}"}

@router.post("/scrape-linkedin", response_model=List[Lead])
async def scrape_linkedin_leads(
    request: LinkedInScrapingRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    if not (request.cookies or (request.email and request.password)):
        raise HTTPException(status_code=400, detail="Either cookies or email/password must be provided")

    if request.proxies:
        lead_scraper.proxies = request.proxies

    async def scrape_and_save():
        try:
            scraped_leads = await lead_scraper.scrape_linkedin(
                request.search_query, 
                request.max_results,
                email=request.email,
                password=request.password,
                cookies=request.cookies
            )
            for lead in scraped_leads:
                lead_service.create_lead(db=db, lead=lead, user_id=current_user.id)
        except Exception as e:
            logging.error(f"Error during LinkedIn scraping: {str(e)}")
            # Here you might want to update the job status or notify the user of the failure

    background_tasks.add_task(scrape_and_save)
    return {"message": f"Scraping {request.max_results} leads from LinkedIn for query: {request.search_query}"}