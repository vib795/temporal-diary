import httpx
from datetime import date
from typing import List, Optional
from dataclasses import dataclass
from app.utils.cache import cache


@dataclass
class HistoricalEvent:
    year: int
    title: str
    description: str
    category: Optional[str] = None
    wikipedia_url: Optional[str] = None
    image_url: Optional[str] = None


@dataclass
class HistoricalFigure:
    name: str
    year: int
    description: str
    event_type: str  # 'birth' or 'death'
    wikipedia_url: Optional[str] = None


class HistoryService:
    """
    Service for fetching historical events for "On This Day" context.
    """

    WIKIPEDIA_API = "https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday"
    MUFFIN_API = "http://history.muffinlabs.com/date"

    def __init__(self, http_client: httpx.AsyncClient):
        self.client = http_client

    @cache(ttl=86400)
    async def get_on_this_day_events(
        self, month: int, day: int, limit: int = 10
    ) -> List[HistoricalEvent]:
        """
        Get historical events that happened on this month/day.
        """
        events = []

        # Try Wikipedia API first
        try:
            response = await self.client.get(
                f"{self.WIKIPEDIA_API}/selected/{month}/{day}",
                headers={"User-Agent": "TemporalDiary/1.0"},
            )

            if response.status_code == 200:
                data = response.json()

                for event in data.get("selected", [])[:limit]:
                    events.append(
                        HistoricalEvent(
                            year=event.get("year", 0),
                            title=event.get("text", ""),
                            description=event.get("text", ""),
                            wikipedia_url=(
                                event.get("pages", [{}])[0]
                                .get("content_urls", {})
                                .get("desktop", {})
                                .get("page")
                                if event.get("pages")
                                else None
                            ),
                        )
                    )
        except Exception as e:
            print(f"Wikipedia API error: {e}")

        # Fallback/supplement with Muffin Labs
        if len(events) < limit:
            try:
                response = await self.client.get(f"{self.MUFFIN_API}/{month}/{day}")

                if response.status_code == 200:
                    data = response.json()

                    for event in data.get("data", {}).get("Events", [])[: limit - len(events)]:
                        events.append(
                            HistoricalEvent(
                                year=int(event.get("year", 0)),
                                title=event.get("text", ""),
                                description=event.get("text", ""),
                            )
                        )
            except Exception as e:
                print(f"Muffin Labs API error: {e}")

        # Sort by year, most recent first
        return sorted(events, key=lambda x: x.year, reverse=True)[:limit]

    @cache(ttl=86400)
    async def get_births_on_this_day(
        self, month: int, day: int, limit: int = 5
    ) -> List[HistoricalFigure]:
        """
        Get notable people born on this day.
        """
        figures = []

        try:
            response = await self.client.get(
                f"{self.WIKIPEDIA_API}/births/{month}/{day}",
                headers={"User-Agent": "TemporalDiary/1.0"},
            )

            if response.status_code == 200:
                data = response.json()

                for birth in data.get("births", [])[:limit]:
                    page = birth.get("pages", [{}])[0] if birth.get("pages") else {}
                    figures.append(
                        HistoricalFigure(
                            name=page.get("title", birth.get("text", "Unknown")),
                            year=birth.get("year", 0),
                            description=birth.get("text", ""),
                            event_type="birth",
                            wikipedia_url=page.get("content_urls", {})
                            .get("desktop", {})
                            .get("page"),
                        )
                    )
        except Exception as e:
            print(f"Births API error: {e}")

        return figures

    @cache(ttl=86400)
    async def get_deaths_on_this_day(
        self, month: int, day: int, limit: int = 5
    ) -> List[HistoricalFigure]:
        """
        Get notable people who died on this day.
        """
        figures = []

        try:
            response = await self.client.get(
                f"{self.WIKIPEDIA_API}/deaths/{month}/{day}",
                headers={"User-Agent": "TemporalDiary/1.0"},
            )

            if response.status_code == 200:
                data = response.json()

                for death in data.get("deaths", [])[:limit]:
                    page = death.get("pages", [{}])[0] if death.get("pages") else {}
                    figures.append(
                        HistoricalFigure(
                            name=page.get("title", death.get("text", "Unknown")),
                            year=death.get("year", 0),
                            description=death.get("text", ""),
                            event_type="death",
                            wikipedia_url=page.get("content_urls", {})
                            .get("desktop", {})
                            .get("page"),
                        )
                    )
        except Exception as e:
            print(f"Deaths API error: {e}")

        return figures

    async def get_year_fact(self, year: int) -> Optional[str]:
        """
        Get an interesting fact about a specific year.
        """
        try:
            response = await self.client.get(f"http://numbersapi.com/{year}/year")
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(f"Year fact API error: {e}")
        return None

    async def get_full_history_context(self, target_date: date) -> dict:
        """
        Get comprehensive historical context for a date.
        """
        month = target_date.month
        day = target_date.day
        year = target_date.year

        events = await self.get_on_this_day_events(month, day)
        births = await self.get_births_on_this_day(month, day)
        deaths = await self.get_deaths_on_this_day(month, day)
        year_fact = await self.get_year_fact(year)

        return {
            "date": target_date.isoformat(),
            "events": events,
            "births": births,
            "deaths": deaths,
            "year_fact": year_fact,
        }
