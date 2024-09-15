from app.worker import celery
from app.services.lead_scraper_service import lead_scraper
from app.services import lead_service
from app.database import SessionLocal

@celery.task(bind=True)
def scrape_linkedin_task(self, user_id: int, search_query: str, max_results: int, email: str = None, password: str = None, cookies: List[Dict] = None):
    try:
        leads = lead_scraper.scrape_linkedin(search_query, max_results, email, password, cookies)
        db = SessionLocal()
        for lead in leads:
            lead_service.create_lead(db=db, lead=lead, user_id=user_id)
        db.close()
        return f"Successfully scraped {len(leads)} leads"
    except Exception as e:
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise