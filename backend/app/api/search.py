from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.meeting_repository import MeetingRepository

router = APIRouter(prefix="/search", tags=["search"])


@router.get("")
def global_search(q: str = Query(min_length=1, max_length=200), limit: int = Query(30, ge=1, le=100), db: Session = Depends(get_db)):
    meetings, transcript_matches = MeetingRepository(db).global_search(q, limit)
    results = [
        {
            "type": "meeting",
            "meeting_id": meeting.id,
            "meeting_title": meeting.title,
            "occurred_at": meeting.occurred_at,
            "participant_names": [link.participant.display_name for link in meeting.participants],
            "snippet": "Meeting title or participant match",
            "start_time_ms": None,
        }
        for meeting in meetings
    ]
    results.extend(
        {
            "type": "transcript",
            "meeting_id": meeting.id,
            "meeting_title": meeting.title,
            "occurred_at": meeting.occurred_at,
            "participant_names": [],
            "snippet": segment.content,
            "speaker_name": segment.speaker_name,
            "start_time_ms": segment.start_time_ms,
        }
        for segment, meeting in transcript_matches
    )
    return {"query": q, "items": results[:limit]}
