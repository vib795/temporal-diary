from sqlalchemy import Column, String, Date, TIMESTAMP, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid

from app.database import Base


class ContextCache(Base):
    __tablename__ = "context_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Cache key components
    context_date = Column(Date, nullable=False, index=True)
    context_type = Column(String(50), nullable=False, index=True)
    location_key = Column(String(100))

    # Cached data
    data = Column(JSONB, nullable=False)

    # Cache management
    cached_at = Column(TIMESTAMP, server_default=func.now())
    expires_at = Column(TIMESTAMP, nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint("context_date", "context_type", "location_key", name="uq_context_cache"),
    )
