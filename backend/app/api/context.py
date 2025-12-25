from fastapi import APIRouter, Query
from datetime import date
from typing import Optional
import httpx

from app.services.nasa_service import NASAService
from app.services.history_service import HistoryService
from app.services.weather_service import WeatherService
from app.services.context_aggregator import ContextAggregator
from app.schemas.context import TemporalContextResponse
from app.config import settings

router = APIRouter(prefix="/context", tags=["context"])

# Create HTTP client (in production, this should be a dependency)
http_client = httpx.AsyncClient(timeout=30.0)

# Initialize services
nasa_service = NASAService(http_client)
history_service = HistoryService(http_client)
weather_service = WeatherService(http_client)
aggregator = ContextAggregator(nasa_service, history_service, weather_service)


@router.get("/{target_date}", response_model=TemporalContextResponse)
async def get_full_context(
    target_date: date,
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    location_name: Optional[str] = Query(None),
    include_weather_comparison: bool = Query(False),
):
    """
    Get complete temporal context for a date.
    Includes space, history, and weather data.
    """
    # Use default location if none provided
    lat = latitude or settings.default_latitude
    lon = longitude or settings.default_longitude
    loc_name = location_name or settings.default_location_name

    context = await aggregator.get_full_context(
        target_date=target_date,
        latitude=lat,
        longitude=lon,
        location_name=loc_name,
        include_weather_comparison=include_weather_comparison,
    )

    return context


@router.get("/{target_date}/space")
async def get_space_context(target_date: date):
    """
    Get only space-related context.
    """
    return await aggregator.get_space_only(target_date)


@router.get("/{target_date}/history")
async def get_history_context(target_date: date):
    """
    Get only historical context.
    """
    return await aggregator.get_history_only(target_date)


@router.get("/{target_date}/weather")
async def get_weather_context(
    target_date: date,
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
    location_name: Optional[str] = Query(None),
):
    """
    Get only weather context.
    """
    lat = latitude or settings.default_latitude
    lon = longitude or settings.default_longitude
    loc_name = location_name or settings.default_location_name

    weather = await weather_service.get_historical_weather(
        target_date, lat, lon, loc_name
    )

    return {"weather": weather, "date": target_date}
