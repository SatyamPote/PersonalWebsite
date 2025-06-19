from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class SavedLinkBase(BaseModel):
    url: HttpUrl
    title: str
    description: Optional[str] = None
    category: Optional[str] = None

class SavedLinkCreate(SavedLinkBase):
    pass

class SavedLink(SavedLinkBase):
    id: int
    owner_id: int
    created_at: datetime
    class Config: from_attributes = True