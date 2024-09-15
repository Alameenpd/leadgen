from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    subscription_plan = Column(String, default="none")
    subscription_start_date = Column(DateTime)
    subscription_end_date = Column(DateTime)
    lemonsqueezy_customer_id = Column(String)

    leads = relationship("Lead", back_populates="owner")
    campaigns = relationship("Campaign", back_populates="owner")
    analytics = relationship("Analytics", back_populates="user")