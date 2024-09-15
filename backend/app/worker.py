from celery import Celery
from app.core.config import settings

celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

celery.conf.task_routes = {
    "app.tasks.scraping_tasks.*": {"queue": "scraping"},
    "app.tasks.campaign_tasks.*": {"queue": "campaigns"},
}

celery.conf.update(task_track_started=True)