from pydantic import BaseModel, EmailStr

class LeadBase(BaseModel):
    name: str
    email: EmailStr | None = None
    twitter_handle: str | None = None
    linkedin_url: str | None = None
    company: str | None = None
    position: str | None = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    pass

class Lead(LeadBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True