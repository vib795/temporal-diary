import httpx
from datetime import date
from typing import Optional
from dataclasses import dataclass
from app.utils.cache import cache


# WMO Weather Codes mapping
WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


@dataclass
class HistoricalWeather:
    date: date
    location_name: Optional[str]
    latitude: float
    longitude: float

    temperature_max_c: float
    temperature_min_c: float
    temperature_mean_c: float

    precipitation_mm: float
    weather_code: int
    weather_description: str

    sunrise: Optional[str]
    sunset: Optional[str]
    daylight_hours: Optional[float]


class WeatherService:
    """
    Service for fetching historical weather data.
    Uses Open-Meteo's free historical weather API.
    """

    BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

    def __init__(self, http_client: httpx.AsyncClient):
        self.client = http_client

    @cache(ttl=86400)  # Weather data doesn't change, cache for 24h
    async def get_historical_weather(
        self,
        target_date: date,
        latitude: float,
        longitude: float,
        location_name: Optional[str] = None,
    ) -> Optional[HistoricalWeather]:
        """
        Get historical weather for a specific date and location.
        Open-Meteo has data from 1940 onwards.
        """
        # Check date bounds
        if target_date < date(1940, 1, 1) or target_date >= date.today():
            return None

        try:
            response = await self.client.get(
                self.BASE_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "start_date": target_date.isoformat(),
                    "end_date": target_date.isoformat(),
                    "daily": "temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,weathercode,sunrise,sunset,daylight_duration",
                    "timezone": "auto",
                },
            )

            if response.status_code != 200:
                return None

            data = response.json()
            daily = data.get("daily", {})

            if not daily or not daily.get("time"):
                return None

            weather_code = daily.get("weathercode", [0])[0] or 0
            daylight_seconds = daily.get("daylight_duration", [0])[0] or 0

            return HistoricalWeather(
                date=target_date,
                location_name=location_name,
                latitude=latitude,
                longitude=longitude,
                temperature_max_c=daily.get("temperature_2m_max", [None])[0],
                temperature_min_c=daily.get("temperature_2m_min", [None])[0],
                temperature_mean_c=daily.get("temperature_2m_mean", [None])[0],
                precipitation_mm=daily.get("precipitation_sum", [0])[0] or 0,
                weather_code=weather_code,
                weather_description=WMO_CODES.get(weather_code, "Unknown"),
                sunrise=daily.get("sunrise", [None])[0],
                sunset=daily.get("sunset", [None])[0],
                daylight_hours=(
                    round(daylight_seconds / 3600, 2) if daylight_seconds else None
                ),
            )

        except Exception as e:
            print(f"Weather fetch error: {e}")
            return None

    async def get_weather_comparison(
        self, target_date: date, latitude: float, longitude: float, years_back: int = 5
    ) -> dict:
        """
        Get weather for the same date across multiple years.
        Useful for "On this day" comparisons.
        """
        comparisons = {}

        for years_ago in range(0, years_back + 1):
            compare_date = target_date.replace(year=target_date.year - years_ago)

            # Handle leap year edge case
            try:
                weather = await self.get_historical_weather(compare_date, latitude, longitude)
                if weather:
                    comparisons[compare_date.year] = weather
            except ValueError:
                # Skip Feb 29 on non-leap years
                continue

        return comparisons
