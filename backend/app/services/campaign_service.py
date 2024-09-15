from pydantic import BaseModel
from datetime import datetime
from typing import List

class CampaignBase(BaseModel):
    name: str
    description: str
    message_template: str
    start_date: datetime
    end_date: datetime

class CampaignCreate(CampaignBase):
    pass

class Campaign(CampaignBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class CampaignWithLeads(Campaign):
    leads: List[int]  # List of lead IDs