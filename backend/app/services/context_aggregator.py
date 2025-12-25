from datetime import date
from typing import Optional, List
from dataclasses import dataclass, field
import asyncio

from app.services.nasa_service import NASAService, APODData, MarsPhoto, NearEarthObject
from app.services.history_service import HistoryService, HistoricalEvent, HistoricalFigure
from app.services.weather_service import WeatherService, HistoricalWeather


@dataclass
class TemporalContext:
    """
    The complete temporal context for a journal entry date.
    Everything happening in space, history, and weather on this day.
    """

    date: date

    # Space context
    apod: Optional[APODData] = None
    mars_photos: List[MarsPhoto] = field(default_factory=list)
    near_earth_objects: List[NearEarthObject] = field(default_factory=list)

    # Historical context
    historical_events: List[HistoricalEvent] = field(default_factory=list)
    notable_births: List[HistoricalFigure] = field(default_factory=list)
    notable_deaths: List[HistoricalFigure] = field(default_factory=list)
    year_fact: Optional[str] = None

    # Weather context
    weather: Optional[HistoricalWeather] = None
    weather_comparison: dict = field(default_factory=dict)

    # Computed insights
    cosmic_perspective: Optional[str] = None
    day_summary: Optional[str] = None


class ContextAggregator:
    """
    Aggregates context from all sources for a given date.
    The brain that combines space, history, and weather into
    a cohesive temporal context.
    """

    def __init__(
        self,
        nasa_service: NASAService,
        history_service: HistoryService,
        weather_service: WeatherService,
    ):
        self.nasa = nasa_service
        self.history = history_service
        self.weather = weather_service

    async def get_full_context(
        self,
        target_date: date,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        location_name: Optional[str] = None,
        include_weather_comparison: bool = False,
    ) -> TemporalContext:
        """
        Fetch all context for a date in parallel.
        """
        # Build tasks
        tasks = {
            "apod": self.nasa.get_apod(target_date),
            "mars": self.nasa.get_mars_photos(target_date),
            "neos": self.nasa.get_near_earth_objects(target_date),
            "events": self.history.get_on_this_day_events(target_date.month, target_date.day),
            "births": self.history.get_births_on_this_day(target_date.month, target_date.day),
            "deaths": self.history.get_deaths_on_this_day(target_date.month, target_date.day),
            "year_fact": self.history.get_year_fact(target_date.year),
        }

        # Add weather if location provided
        if latitude and longitude:
            tasks["weather"] = self.weather.get_historical_weather(
                target_date, latitude, longitude, location_name
            )
            if include_weather_comparison:
                tasks["weather_comparison"] = self.weather.get_weather_comparison(
                    target_date, latitude, longitude
                )

        # Execute all tasks concurrently
        results = {}
        task_items = list(tasks.items())
        task_results = await asyncio.gather(
            *[task for _, task in task_items], return_exceptions=True
        )

        for (key, _), result in zip(task_items, task_results):
            if isinstance(result, Exception):
                print(f"Error fetching {key}: {result}")
                results[key] = None
            else:
                results[key] = result

        # Build context object
        context = TemporalContext(
            date=target_date,
            apod=results.get("apod"),
            mars_photos=results.get("mars") or [],
            near_earth_objects=results.get("neos") or [],
            historical_events=results.get("events") or [],
            notable_births=results.get("births") or [],
            notable_deaths=results.get("deaths") or [],
            year_fact=results.get("year_fact"),
            weather=results.get("weather"),
            weather_comparison=results.get("weather_comparison") or {},
        )

        # Generate summary
        context.day_summary = self._generate_day_summary(context)

        return context

    def _generate_day_summary(self, context: TemporalContext) -> str:
        """
        Generate a brief poetic summary of the day's context.
        """
        parts = []

        # Space
        if context.apod:
            parts.append(f"In space: NASA featured '{context.apod.title}'")

        if context.near_earth_objects:
            closest = context.near_earth_objects[0]
            parts.append(
                f"An asteroid ({closest.name}) passed {closest.miss_distance_km:,.0f} km from Earth"
            )

        # History
        if context.historical_events:
            top_event = context.historical_events[0]
            parts.append(f"In {top_event.year}: {top_event.title[:100]}")

        # Weather
        if context.weather:
            parts.append(
                f"Weather: {context.weather.weather_description}, "
                f"{context.weather.temperature_mean_c:.1f}°C"
            )

        return " • ".join(parts) if parts else "Another day in the cosmic journey."

    async def get_space_only(self, target_date: date) -> dict:
        """Get just space context."""
        return await self.nasa.get_space_context(target_date)

    async def get_history_only(self, target_date: date) -> dict:
        """Get just historical context."""
        return await self.history.get_full_history_context(target_date)

    async def get_memories(self, user_entries: List[dict], target_date: date) -> List[dict]:
        """
        Find user's entries from the same day in previous years.
        """
        memories = []
        target_month_day = (target_date.month, target_date.day)

        for entry in user_entries:
            entry_date = entry.get("entry_date")
            if isinstance(entry_date, str):
                from datetime import datetime

                entry_date = datetime.strptime(entry_date, "%Y-%m-%d").date()

            if (entry_date.month, entry_date.day) == target_month_day:
                if entry_date.year != target_date.year:
                    memories.append(
                        {
                            "entry": entry,
                            "years_ago": target_date.year - entry_date.year,
                        }
                    )

        return sorted(memories, key=lambda x: x["years_ago"])
