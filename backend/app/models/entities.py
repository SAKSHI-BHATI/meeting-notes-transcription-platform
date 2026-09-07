from __future__ import annotations
from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class User(Timestamped, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    meetings: Mapped[list[Meeting]] = relationship(back_populates="owner")


class Meeting(Timestamped, Base):
    __tablename__ = "meetings"
    __table_args__ = (Index("ix_meetings_owner_occurred", "owner_id", "occurred_at"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    duration_ms: Mapped[int] = mapped_column(Integer, default=0)
    source: Mapped[str] = mapped_column(String(30), default="uploaded")
    owner: Mapped[User] = relationship(back_populates="meetings")
    participants: Mapped[list[MeetingParticipant]] = relationship(back_populates="meeting", cascade="all, delete-orphan")
    segments: Mapped[list[TranscriptSegment]] = relationship(back_populates="meeting", cascade="all, delete-orphan", order_by="TranscriptSegment.start_time_ms")
    summary: Mapped[Summary | None] = relationship(back_populates="meeting", cascade="all, delete-orphan", uselist=False)
    topics: Mapped[list[Topic]] = relationship(back_populates="meeting", cascade="all, delete-orphan")
    action_items: Mapped[list[ActionItem]] = relationship(back_populates="meeting", cascade="all, delete-orphan")


class Participant(Timestamped, Base):
    __tablename__ = "participants"
    id: Mapped[int] = mapped_column(primary_key=True)
    display_name: Mapped[str] = mapped_column(String(120), index=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    initials: Mapped[str] = mapped_column(String(4))
    color: Mapped[str] = mapped_column(String(16), default="#6D5CE7")
    meetings: Mapped[list[MeetingParticipant]] = relationship(back_populates="participant")


class MeetingParticipant(Base):
    __tablename__ = "meeting_participants"
    __table_args__ = (UniqueConstraint("meeting_id", "participant_id", name="uq_meeting_participant"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), index=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("participants.id"), index=True)
    role: Mapped[str] = mapped_column(String(30), default="attendee")
    meeting: Mapped[Meeting] = relationship(back_populates="participants")
    participant: Mapped[Participant] = relationship(back_populates="meetings")


class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"
    __table_args__ = (Index("ix_segments_meeting_start", "meeting_id", "start_time_ms"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), index=True)
    speaker_id: Mapped[int | None] = mapped_column(ForeignKey("participants.id"))
    speaker_name: Mapped[str] = mapped_column(String(120))
    start_time_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    meeting: Mapped[Meeting] = relationship(back_populates="segments")


class Summary(Timestamped, Base):
    __tablename__ = "summaries"
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), primary_key=True)
    overview: Mapped[str] = mapped_column(Text)
    key_points_json: Mapped[str] = mapped_column(Text, default="[]")
    decisions_json: Mapped[str] = mapped_column(Text, default="[]")
    provider: Mapped[str] = mapped_column(String(50), default="mock")
    meeting: Mapped[Meeting] = relationship(back_populates="summary")


class Topic(Base):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), index=True)
    label: Mapped[str] = mapped_column(String(120))
    start_time_ms: Mapped[int | None] = mapped_column(Integer)
    meeting: Mapped[Meeting] = relationship(back_populates="topics")


class ActionItem(Timestamped, Base):
    __tablename__ = "action_items"
    __table_args__ = (Index("ix_action_items_meeting_status", "meeting_id", "status"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id", ondelete="CASCADE"), index=True)
    assignee_id: Mapped[int | None] = mapped_column(ForeignKey("participants.id"))
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text)
    due_date: Mapped[date | None] = mapped_column(Date)
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    status: Mapped[str] = mapped_column(String(20), default="open")
    meeting: Mapped[Meeting] = relationship(back_populates="action_items")
    assignee: Mapped[Participant | None] = relationship()
