from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date


class APODResponse(BaseModel):
    date: date
    title: str
    explanation: str
    url: str
    hdurl: Optional[str] = None
    media_type: str
    copyright: Optional[str] = None


class MarsPhotoResponse(BaseModel):
    id: int
    sol: int
    earth_date: date
    camera_name: str
    camera_full_name: str
    rover_name: str
    img_src: str


class NearEarthObjectResponse(BaseModel):
    id: str
    name: str
    nasa_jpl_url: str
    estimated_diameter_min_m: float
    estimated_diameter_max_m: float
    is_potentially_hazardous: bool
    close_approach_date: date
    miss_distance_km: float
    relative_velocity_kph: float


class HistoricalEventResponse(BaseModel):
    year: int
    title: str
    description: str
    category: Optional[str] = None
    wikipedia_url: Optional[str] = None
    image_url: Optional[str] = None


class HistoricalFigureResponse(BaseModel):
    name: str
    year: int
    description: str
    event_type: str
    wikipedia_url: Optional[str] = None


class HistoricalWeatherResponse(BaseModel):
    date: date
    location_name: Optional[str] = None
    latitude: float
    longitude: float
    temperature_max_c: float
    temperature_min_c: float
    temperature_mean_c: float
    precipitation_mm: float
    weather_code: int
    weather_description: str
    sunrise: Optional[str] = None
    sunset: Optional[str] = None
    daylight_hours: Optional[float] = None


class TemporalContextResponse(BaseModel):
    date: date
    apod: Optional[APODResponse] = None
    mars_photos: List[MarsPhotoResponse] = []
    near_earth_objects: List[NearEarthObjectResponse] = []
    historical_events: List[HistoricalEventResponse] = []
    notable_births: List[HistoricalFigureResponse] = []
    notable_deaths: List[HistoricalFigureResponse] = []
    year_fact: Optional[str] = None
    weather: Optional[HistoricalWeatherResponse] = None
    weather_comparison: Dict[int, HistoricalWeatherResponse] = {}
    cosmic_perspective: Optional[str] = None
    day_summary: Optional[str] = None
