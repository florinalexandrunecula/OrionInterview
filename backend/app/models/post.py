from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    author: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: Optional[datetime] = None
    