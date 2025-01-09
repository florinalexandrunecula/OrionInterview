from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str
    content: str
    author: Optional[str] = None
    created_at: datetime | None  = None
    updated_at: Optional[datetime] = None
    photo: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    photo: Optional[str] = None
    