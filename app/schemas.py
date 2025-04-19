from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class NewsBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: str
    publishedAt: datetime

    model_config = ConfigDict(from_attributes=True)


# For creating news entries
class NewsCreate(NewsBase):
    pass


# For response model
class News(NewsBase):
    id: int

    class Config:
        orm_mode = True
