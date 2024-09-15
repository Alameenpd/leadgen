from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Analytics(Base):
    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    leads_scraped = Column(Integer, default=0)
    messages_sent = Column(Integer, default=0)
    responses_received = Column(Integer, default=0)
    conversion_rate = Column(Float, default=0.0)
    date = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)  # For storing additional analytics data

    user = relationship("User", back_populates="analytics")
    campaign = relationship("Campaign", back_populates="analytics")