from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID
import uuid

from app.database import get_db
from app.models.entry import Entry
from app.schemas.entry import EntryCreate, EntryUpdate, EntryResponse, EntryListResponse

router = APIRouter(prefix="/entries", tags=["entries"])


# For MVP, using a demo user ID. In production, get from auth token
DEMO_USER_ID = uuid.uuid4()


@router.get("/", response_model=EntryListResponse)
async def list_entries(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """
    List user's entries (paginated).
    """
    offset = (page - 1) * page_size

    # Get entries
    result = await db.execute(
        select(Entry)
        .where(Entry.user_id == DEMO_USER_ID)
        .order_by(Entry.entry_date.desc())
        .offset(offset)
        .limit(page_size)
    )
    entries = result.scalars().all()

    # Get total count
    count_result = await db.execute(
        select(Entry).where(Entry.user_id == DEMO_USER_ID)
    )
    total = len(count_result.scalars().all())

    return EntryListResponse(
        entries=entries,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/today", response_model=Optional[EntryResponse])
async def get_today_entry(db: AsyncSession = Depends(get_db)):
    """
    Get entry for today's date.
    """
    today = date.today()
    result = await db.execute(
        select(Entry).where(
            and_(Entry.user_id == DEMO_USER_ID, Entry.entry_date == today)
        )
    )
    entry = result.scalar_one_or_none()
    return entry


@router.get("/{entry_date}", response_model=Optional[EntryResponse])
async def get_entry(entry_date: date, db: AsyncSession = Depends(get_db)):
    """
    Get entry for a specific date.
    """
    result = await db.execute(
        select(Entry).where(
            and_(Entry.user_id == DEMO_USER_ID, Entry.entry_date == entry_date)
        )
    )
    entry = result.scalar_one_or_none()
    return entry


@router.post("/", response_model=EntryResponse, status_code=201)
async def create_entry(entry_data: EntryCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a new entry.
    """
    # Check if entry already exists for this date
    existing = await db.execute(
        select(Entry).where(
            and_(Entry.user_id == DEMO_USER_ID, Entry.entry_date == entry_data.entry_date)
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Entry already exists for this date")

    # Calculate word count
    word_count = len(entry_data.content.split()) if entry_data.content else 0

    # Create entry
    entry = Entry(
        user_id=DEMO_USER_ID,
        entry_date=entry_data.entry_date,
        title=entry_data.title,
        content=entry_data.content,
        mood=entry_data.mood,
        mood_score=entry_data.mood_score,
        latitude=entry_data.latitude,
        longitude=entry_data.longitude,
        location_name=entry_data.location_name,
        tags=entry_data.tags,
        is_private=entry_data.is_private,
        word_count=word_count,
    )

    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    return entry


@router.put("/{entry_date}", response_model=EntryResponse)
async def update_entry(
    entry_date: date, entry_data: EntryUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update an existing entry.
    """
    result = await db.execute(
        select(Entry).where(
            and_(Entry.user_id == DEMO_USER_ID, Entry.entry_date == entry_date)
        )
    )
    entry = result.scalar_one_or_none()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    # Update fields
    update_data = entry_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entry, field, value)

    # Recalculate word count if content changed
    if "content" in update_data:
        entry.word_count = len(entry.content.split()) if entry.content else 0

    entry.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(entry)

    return entry


@router.delete("/{entry_date}", status_code=204)
async def delete_entry(entry_date: date, db: AsyncSession = Depends(get_db)):
    """
    Delete an entry.
    """
    result = await db.execute(
        select(Entry).where(
            and_(Entry.user_id == DEMO_USER_ID, Entry.entry_date == entry_date)
        )
    )
    entry = result.scalar_one_or_none()

    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")

    await db.delete(entry)
    await db.commit()

    return None
