from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import date, datetime
from uuid import UUID


class EntryBase(BaseModel):
    entry_date: date
    title: Optional[str] = None
    content: str
    mood: Optional[str] = None
    mood_score: Optional[int] = Field(None, ge=1, le=10)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_name: Optional[str] = None
    tags: List[str] = []
    is_private: bool = True


class EntryCreate(EntryBase):
    pass


class EntryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood: Optional[str] = None
    mood_score: Optional[int] = Field(None, ge=1, le=10)
    tags: Optional[List[str]] = None
    is_private: Optional[bool] = None


class EntryResponse(EntryBase):
    id: UUID
    user_id: UUID
    content_html: Optional[str] = None
    word_count: Optional[int] = None
    writing_time_seconds: Optional[int] = None
    context_snapshot: Optional[Any] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EntryListResponse(BaseModel):
    entries: List[EntryResponse]
    total: int
    page: int
    page_size: int
