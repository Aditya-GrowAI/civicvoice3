from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
import uuid
from datetime import datetime

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True

class Issue(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str # 'Manual' or 'Detected'
    lat: float
    lng: float
    status: str = "Pending"
    image: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[str] = None # Link to Clerk User ID (sub)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True