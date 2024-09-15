from app.worker import celery
from app.services.dm_service import dm_service
from app.database import SessionLocal
from app.models.campaign import Campaign

@celery.task(bind=True)
def send_campaign_dms(self, campaign_id: int, email: str, password: str):
    db = SessionLocal()
    try:
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        if not campaign:
            raise ValueError(f"Campaign with id {campaign_id} not found")
        
        asyncio.run(dm_service.process_campaign(campaign, email, password))
        return f"Successfully processed campaign {campaign_id}"
    except Exception as e:
        self.update_state(state='FAILURE', meta={'exc': str(e)})
        raise
    finally:
        db.close()