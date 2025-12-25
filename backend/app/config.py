from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/temporal_diary"
    database_url_sync: str = "postgresql://postgres:password@localhost:5432/temporal_diary"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # API Keys
    nasa_api_key: str = "DEMO_KEY"
    openai_api_key: str = ""

    # App Settings
    secret_key: str = "your-super-secret-key-change-in-production"
    cors_origins: str = '["http://localhost:5173","http://localhost:3000"]'
    debug: bool = True

    # Default Location
    default_latitude: float = 30.2672
    default_longitude: float = -97.7431
    default_location_name: str = "Austin, TX"

    # Cache TTL
    context_cache_ttl: int = 86400
    weather_cache_ttl: int = 86400

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from JSON string"""
        try:
            return json.loads(self.cors_origins)
        except:
            return ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()
