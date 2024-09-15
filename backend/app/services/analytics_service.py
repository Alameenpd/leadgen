from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.analytics import Analytics
from datetime import datetime, timedelta

def update_analytics(db: Session, user_id: int, campaign_id: int, leads_scraped: int = 0, messages_sent: int = 0, responses_received: int = 0, metadata: dict = None):
    analytics = db.query(Analytics).filter(Analytics.user_id == user_id, Analytics.campaign_id == campaign_id, Analytics.date == datetime.utcnow().date()).first()
    
    if not analytics:
        analytics = Analytics(user_id=user_id, campaign_id=campaign_id)
        db.add(analytics)
    
    analytics.leads_scraped += leads_scraped
    analytics.messages_sent += messages_sent
    analytics.responses_received += responses_received
    
    if analytics.messages_sent > 0:
        analytics.conversion_rate = (analytics.responses_received / analytics.messages_sent) * 100
    
    if metadata:
        analytics.metadata = analytics.metadata or {}
        analytics.metadata.update(metadata)
    
    db.commit()
    db.refresh(analytics)
    return analytics

def get_user_analytics(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return db.query(Analytics).filter(
        Analytics.user_id == user_id,
        Analytics.date >= start_date,
        Analytics.date <= end_date
    ).all()

def get_campaign_analytics(db: Session, campaign_id: int, start_date: datetime, end_date: datetime):
    return db.query(Analytics).filter(
        Analytics.campaign_id == campaign_id,
        Analytics.date >= start_date,
        Analytics.date <= end_date
    ).all()

def get_overall_stats(db: Session, user_id: int):
    return db.query(
        func.sum(Analytics.leads_scraped).label("total_leads_scraped"),
        func.sum(Analytics.messages_sent).label("total_messages_sent"),
        func.sum(Analytics.responses_received).label("total_responses_received"),
        (func.sum(Analytics.responses_received) / func.sum(Analytics.messages_sent) * 100).label("overall_conversion_rate")
    ).filter(Analytics.user_id == user_id).first()

def get_daily_stats(db: Session, user_id: int, days: int = 30):
    start_date = datetime.utcnow() - timedelta(days=days)
    return db.query(
        Analytics.date,
        func.sum(Analytics.leads_scraped).label("leads_scraped"),
        func.sum(Analytics.messages_sent).label("messages_sent"),
        func.sum(Analytics.responses_received).label("responses_received"),
        (func.sum(Analytics.responses_received) / func.sum(Analytics.messages_sent) * 100).label("conversion_rate")
    ).filter(
        Analytics.user_id == user_id,
        Analytics.date >= start_date
    ).group_by(Analytics.date).order_by(Analytics.date).all()