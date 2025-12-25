import httpx
from datetime import date, datetime
from typing import Optional, List
from dataclasses import dataclass
from app.config import settings
from app.utils.cache import cache


@dataclass
class APODData:
    date: date
    title: str
    explanation: str
    url: str
    hdurl: Optional[str]
    media_type: str  # 'image' or 'video'
    copyright: Optional[str]


@dataclass
class MarsPhoto:
    id: int
    sol: int
    earth_date: date
    camera_name: str
    camera_full_name: str
    rover_name: str
    img_src: str


@dataclass
class NearEarthObject:
    id: str
    name: str
    nasa_jpl_url: str
    estimated_diameter_min_m: float
    estimated_diameter_max_m: float
    is_potentially_hazardous: bool
    close_approach_date: date
    miss_distance_km: float
    relative_velocity_kph: float


class NASAService:
    """
    Service for fetching NASA data to provide cosmic context.
    """

    BASE_URL = "https://api.nasa.gov"

    def __init__(self, http_client: httpx.AsyncClient):
        self.client = http_client
        self.api_key = settings.nasa_api_key

    @cache(ttl=86400)  # Cache for 24 hours
    async def get_apod(self, target_date: date) -> Optional[APODData]:
        """
        Get Astronomy Picture of the Day for a specific date.
        Available from June 16, 1995 onwards.
        """
        # APOD started June 16, 1995
        apod_start = date(1995, 6, 16)
        if target_date < apod_start or target_date > date.today():
            return None

        try:
            response = await self.client.get(
                f"{self.BASE_URL}/planetary/apod",
                params={
                    "api_key": self.api_key,
                    "date": target_date.isoformat(),
                },
            )

            if response.status_code != 200:
                return None

            data = response.json()

            return APODData(
                date=datetime.strptime(data["date"], "%Y-%m-%d").date(),
                title=data["title"],
                explanation=data["explanation"],
                url=data["url"],
                hdurl=data.get("hdurl"),
                media_type=data["media_type"],
                copyright=data.get("copyright"),
            )
        except Exception as e:
            print(f"APOD fetch error: {e}")
            return None

    @cache(ttl=86400)
    async def get_mars_photos(
        self, target_date: date, rover: str = "curiosity"
    ) -> List[MarsPhoto]:
        """
        Get Mars rover photos for a specific Earth date.
        """
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/mars-photos/api/v1/rovers/{rover}/photos",
                params={
                    "api_key": self.api_key,
                    "earth_date": target_date.isoformat(),
                },
            )

            if response.status_code != 200:
                return []

            data = response.json()
            photos = []

            for photo in data.get("photos", [])[:5]:  # Limit to 5
                photos.append(
                    MarsPhoto(
                        id=photo["id"],
                        sol=photo["sol"],
                        earth_date=datetime.strptime(photo["earth_date"], "%Y-%m-%d").date(),
                        camera_name=photo["camera"]["name"],
                        camera_full_name=photo["camera"]["full_name"],
                        rover_name=photo["rover"]["name"],
                        img_src=photo["img_src"],
                    )
                )

            return photos
        except Exception as e:
            print(f"Mars photos fetch error: {e}")
            return []

    @cache(ttl=3600)  # Cache for 1 hour (for today's date)
    async def get_near_earth_objects(self, target_date: date) -> List[NearEarthObject]:
        """
        Get asteroids passing near Earth on a specific date.
        """
        try:
            response = await self.client.get(
                f"{self.BASE_URL}/neo/rest/v1/feed",
                params={
                    "api_key": self.api_key,
                    "start_date": target_date.isoformat(),
                    "end_date": target_date.isoformat(),
                },
            )

            if response.status_code != 200:
                return []

            data = response.json()
            neos = []

            date_key = target_date.isoformat()
            for neo in data.get("near_earth_objects", {}).get(date_key, []):
                approach = neo["close_approach_data"][0] if neo["close_approach_data"] else {}
                diameter = neo["estimated_diameter"]["meters"]

                neos.append(
                    NearEarthObject(
                        id=neo["id"],
                        name=neo["name"],
                        nasa_jpl_url=neo["nasa_jpl_url"],
                        estimated_diameter_min_m=diameter["estimated_diameter_min"],
                        estimated_diameter_max_m=diameter["estimated_diameter_max"],
                        is_potentially_hazardous=neo["is_potentially_hazardous_asteroid"],
                        close_approach_date=target_date,
                        miss_distance_km=float(
                            approach.get("miss_distance", {}).get("kilometers", 0)
                        ),
                        relative_velocity_kph=float(
                            approach.get("relative_velocity", {}).get("kilometers_per_hour", 0)
                        ),
                    )
                )

            return sorted(neos, key=lambda x: x.miss_distance_km)[:5]
        except Exception as e:
            print(f"NEO fetch error: {e}")
            return []

    async def get_space_context(self, target_date: date) -> dict:
        """
        Get comprehensive space context for a date.
        """
        apod = await self.get_apod(target_date)
        mars_photos = await self.get_mars_photos(target_date)
        neos = await self.get_near_earth_objects(target_date)

        return {
            "apod": apod,
            "mars_photos": mars_photos,
            "near_earth_objects": neos,
            "date": target_date.isoformat(),
        }
