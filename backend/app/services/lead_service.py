from sqlalchemy.orm import Session
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate

def get_leads(db: Session, skip: int = 0, limit: int = 100, user_id: int = None):
    query = db.query(Lead)
    if user_id:
        query = query.filter(Lead.owner_id == user_id)
    return query.offset(skip).limit(limit).all()

def get_lead(db: Session, lead_id: int):
    return db.query(Lead).filter(Lead.id == lead_id).first()

def create_lead(db: Session, lead: LeadCreate, user_id: int):
    db_lead = Lead(**lead.dict(), owner_id=user_id)
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def update_lead(db: Session, lead_id: int, lead: LeadUpdate):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if db_lead:
        update_data = lead.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_lead, key, value)
        db.commit()
        db.refresh(db_lead)
    return db_lead

def delete_lead(db: Session, lead_id: int):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if db_lead:
        db.delete(db_lead)
        db.commit()
    return db_lead