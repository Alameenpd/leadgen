from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String)
    twitter_handle = Column(String)
    linkedin_url = Column(String)
    company = Column(String)
    position = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="leads")
    campaigns = relationship("Campaign", secondary="campaign_leads", back_populates="leads")