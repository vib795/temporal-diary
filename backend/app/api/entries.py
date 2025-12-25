from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from datetime import date, datetime
from uuid import UUID
import uuid
import httpx

from app.database import get_db
from app.models.entry import Entry
from app.schemas.entry import EntryCreate, EntryUpdate, EntryResponse, EntryListResponse
from app.services.nasa_service import NASAService
from app.services.history_service import HistoryService
from app.services.weather_service import WeatherService
from app.services.context_aggregator import ContextAggregator
from app.config import settings

router = APIRouter(prefix="/entries", tags=["entries"])

# Initialize services for context fetching
http_client = httpx.AsyncClient(timeout=30.0)
nasa_service = NASAService(http_client)
history_service = HistoryService(http_client)
weather_service = WeatherService(http_client)
aggregator = ContextAggregator(nasa_service, history_service, weather_service)

# For MVP, using a demo user ID. In production, get from auth token
DEMO_USER_ID = uuid.uuid4()


async def fetch_and_serialize_context(entry_date: date) -> dict:
    """Fetch context and convert to JSON-serializable dict"""
    context = await aggregator.get_full_context(
        target_date=entry_date,
        latitude=settings.default_latitude,
        longitude=settings.default_longitude,
        location_name=settings.default_location_name,
    )

    # Convert dataclasses to dicts
    from dataclasses import asdict
    context_dict = {}

    if context.apod:
        context_dict["apod"] = asdict(context.apod)
        context_dict["apod"]["date"] = context_dict["apod"]["date"].isoformat()

    context_dict["mars_photos"] = [
        {**asdict(p), "earth_date": p.earth_date.isoformat()}
        for p in context.mars_photos
    ]

    context_dict["near_earth_objects"] = [
        {**asdict(n), "close_approach_date": n.close_approach_date.isoformat()}
        for n in context.near_earth_objects
    ]

    context_dict["historical_events"] = [asdict(e) for e in context.historical_events]
    context_dict["notable_births"] = [asdict(f) for f in context.notable_births]
    context_dict["notable_deaths"] = [asdict(f) for f in context.notable_deaths]
    context_dict["year_fact"] = context.year_fact

    if context.weather:
        weather_dict = asdict(context.weather)
        weather_dict["date"] = weather_dict["date"].isoformat()
        context_dict["weather"] = weather_dict

    context_dict["day_summary"] = context.day_summary

    return context_dict


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

    # Fetch and save context snapshot
    context_snapshot = await fetch_and_serialize_context(entry_data.entry_date)

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
        context_snapshot=context_snapshot,
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

    # Save context snapshot if it doesn't exist yet (for existing entries)
    if not entry.context_snapshot:
        entry.context_snapshot = await fetch_and_serialize_context(entry_date)

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
