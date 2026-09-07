from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import ORMModel


class ParticipantInput(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str | None = None


class ParticipantRead(ORMModel):
    id: int
    display_name: str
    email: str | None
    initials: str
    color: str


class MeetingCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    occurred_at: datetime
    duration_ms: int = Field(default=0, ge=0)
    participant_names: list[str] = Field(default_factory=list, max_length=30)
    transcript_text: str | None = Field(default=None, max_length=200_000)


class MeetingUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    occurred_at: datetime | None = None
    duration_ms: int | None = Field(default=None, ge=0)
    participant_names: list[str] | None = Field(default=None, max_length=30)


class MeetingListItem(ORMModel):
    id: int
    title: str
    occurred_at: datetime
    duration_ms: int
    source: str
    participant_names: list[str] = []
    action_item_count: int = 0


class MeetingRead(MeetingListItem):
    created_at: datetime
    updated_at: datetime


class SegmentCreate(BaseModel):
    speaker_name: str = Field(min_length=1, max_length=120)
    start_time_ms: int = Field(ge=0)
    end_time_ms: int = Field(ge=0)
    content: str = Field(min_length=1, max_length=10_000)


class SegmentRead(ORMModel):
    id: int
    speaker_name: str
    start_time_ms: int
    end_time_ms: int
    content: str


class TranscriptRead(BaseModel):
    meeting_id: int
    items: list[SegmentRead]


class SummaryRead(ORMModel):
    meeting_id: int
    overview: str
    key_points: list[str]
    decisions: list[str]
    provider: str


class TopicRead(ORMModel):
    id: int
    label: str
    start_time_ms: int | None
