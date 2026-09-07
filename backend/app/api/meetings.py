import json
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.meeting import MeetingCreate, MeetingListItem, MeetingRead, MeetingUpdate, SegmentRead, SummaryRead, TopicRead, TranscriptRead
from app.services.meeting_service import MeetingService
from app.services.transcript_parser import parser_for

router = APIRouter(prefix="/meetings", tags=["meetings"])

def serialize_meeting(m): return {"id": m.id, "title": m.title, "occurred_at": m.occurred_at, "duration_ms": m.duration_ms, "source": m.source, "participant_names": [x.participant.display_name for x in m.participants], "action_item_count": len(m.action_items) if hasattr(m, "action_items") else 0, "created_at": m.created_at, "updated_at": m.updated_at}

@router.get("")
def list_meetings(q: str | None = None, participant: str | None = None, page: int = Query(1, ge=1), page_size: int = Query(12, ge=1, le=100), sort: str = Query("recent", pattern="^(recent|oldest|title)$"), db: Session = Depends(get_db)):
    items, total = MeetingService(db).list(query=q, participant=participant, page=page, page_size=page_size, sort=sort)
    return {"items": [serialize_meeting(item) for item in items], "total": total, "page": page, "page_size": page_size}

@router.post("", status_code=201)
def create_meeting(payload: MeetingCreate, db: Session = Depends(get_db)): return serialize_meeting(MeetingService(db).create(payload))

@router.get("/{meeting_id}")
def get_meeting(meeting_id: int, db: Session = Depends(get_db)):
    try: return serialize_meeting(MeetingService(db).get_or_raise(meeting_id))
    except LookupError as error: raise HTTPException(404, detail={"code":"not_found", "message":str(error)})

@router.patch("/{meeting_id}")
def update_meeting(meeting_id: int, payload: MeetingUpdate, db: Session = Depends(get_db)):
    try: return serialize_meeting(MeetingService(db).update(meeting_id, payload))
    except LookupError as error: raise HTTPException(404, detail={"code":"not_found", "message":str(error)})

@router.delete("/{meeting_id}", status_code=204)
def delete_meeting(meeting_id: int, db: Session = Depends(get_db)):
    try: MeetingService(db).delete(meeting_id)
    except LookupError as error: raise HTTPException(404, detail={"code":"not_found", "message":str(error)})

@router.get("/{meeting_id}/transcript")
def transcript(meeting_id: int, q: str | None = None, db: Session = Depends(get_db)):
    service = MeetingService(db)
    try: service.get_or_raise(meeting_id)
    except LookupError as error: raise HTTPException(404, detail={"code":"not_found", "message":str(error)})
    return {"meeting_id": meeting_id, "items": service.repo.segments(meeting_id, q)}


@router.get("/{meeting_id}/transcript/search")
def search_transcript(meeting_id: int, q: str = Query(min_length=1, max_length=200), db: Session = Depends(get_db)):
    """Return matching transcript segments without making the client scan the full transcript."""
    service = MeetingService(db)
    try:
        service.get_or_raise(meeting_id)
    except LookupError as error:
        raise HTTPException(404, detail={"code": "meeting_not_found", "message": str(error)})
    return {"meeting_id": meeting_id, "query": q, "items": service.repo.segments(meeting_id, q)}

@router.post("/{meeting_id}/transcript/upload", status_code=201)
async def upload_transcript(meeting_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename or file.filename.rsplit(".", 1)[-1].lower() not in {"txt", "vtt", "json"}: raise HTTPException(415, detail={"code":"invalid_file", "message":"Use a TXT, VTT, or JSON transcript."})
    raw = await file.read()
    if len(raw) > 2_000_000: raise HTTPException(413, detail={"code":"file_too_large", "message":"Transcript must be 2 MB or smaller."})
    try: segments = parser_for(file.filename).parse(raw.decode("utf-8"))
    except Exception as error: raise HTTPException(422, detail={"code":"invalid_transcript", "message":str(error)})
    try: MeetingService(db).replace_uploaded_transcript(meeting_id, segments)
    except LookupError as error: raise HTTPException(404, detail={"code":"not_found", "message":str(error)})
    return {"segments_created": len(segments)}

@router.get("/{meeting_id}/summary")
def summary(meeting_id: int, db: Session = Depends(get_db)):
    try: meeting = MeetingService(db).get_or_raise(meeting_id)
    except LookupError as error: raise HTTPException(404, detail={"code":"not_found", "message":str(error)})
    if not meeting.summary: raise HTTPException(404, detail={"code":"not_found", "message":"Summary not found"})
    return {"meeting_id": meeting_id, "overview": meeting.summary.overview, "key_points": json.loads(meeting.summary.key_points_json), "decisions": json.loads(meeting.summary.decisions_json), "provider": meeting.summary.provider}

@router.get("/{meeting_id}/topics")
def topics(meeting_id: int, db: Session = Depends(get_db)):
    try: return MeetingService(db).get_or_raise(meeting_id).topics
    except LookupError as error: raise HTTPException(404, detail={"code":"not_found", "message":str(error)})
