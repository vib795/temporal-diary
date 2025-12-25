from sqlalchemy import (
    Column,
    String,
    Text,
    Date,
    Integer,
    DECIMAL,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    ARRAY,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.database import Base


class Entry(Base):
    __tablename__ = "entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # The entry itself
    entry_date = Column(Date, nullable=False, index=True)
    title = Column(String(500))
    content = Column(Text, nullable=False)
    content_html = Column(Text)

    # Mood tracking
    mood = Column(String(50))
    mood_score = Column(Integer, CheckConstraint("mood_score >= 1 AND mood_score <= 10"))

    # Entry metadata
    word_count = Column(Integer)
    writing_time_seconds = Column(Integer)

    # Location context (if different from default)
    latitude = Column(DECIMAL(10, 8))
    longitude = Column(DECIMAL(11, 8))
    location_name = Column(String(255))

    # Tags
    tags = Column(ARRAY(Text), default=[])

    # Privacy
    is_private = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "entry_date", name="uq_user_entry_date"),
    )
