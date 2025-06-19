from pydantic import BaseModel
from datetime import datetime

class MediaFile(BaseModel):
    id: int
    filename: str
    file_url: str
    file_type: str
    created_at: datetime
    owner_id: int

    class Config:
        # This allows Pydantic to read data from ORM models
        from_attributes = True