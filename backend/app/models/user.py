from sqlalchemy import Column, String, DECIMAL, ARRAY, Boolean, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Location for weather context
    default_latitude = Column(DECIMAL(10, 8))
    default_longitude = Column(DECIMAL(11, 8))
    default_location_name = Column(String(255))
    timezone = Column(String(50), default="UTC")

    # Preferences
    preferred_context_types = Column(
        ARRAY(Text), default=["space", "history", "weather"]
    )
    show_cosmic_perspective = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
