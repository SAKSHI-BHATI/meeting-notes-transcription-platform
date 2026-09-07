from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload
from app.models import ActionItem, Meeting, MeetingParticipant, Participant, TranscriptSegment


class MeetingRepository:
    def __init__(self, db: Session): self.db = db

    def list(self, *, query: str | None, participant: str | None, page: int, page_size: int, sort: str):
        statement = select(Meeting).options(selectinload(Meeting.participants).selectinload(MeetingParticipant.participant))
        if query:
            term = f"%{query.strip()}%"
            statement = statement.where(or_(Meeting.title.ilike(term), Meeting.id.in_(select(MeetingParticipant.meeting_id).join(Participant).where(Participant.display_name.ilike(term)))))
        if participant:
            statement = statement.where(Meeting.id.in_(select(MeetingParticipant.meeting_id).join(Participant).where(Participant.display_name.ilike(f"%{participant}%"))))
        total = self.db.scalar(select(func.count()).select_from(statement.subquery())) or 0
        order = Meeting.title.asc() if sort == "title" else Meeting.occurred_at.asc() if sort == "oldest" else Meeting.occurred_at.desc()
        return self.db.scalars(statement.order_by(order).offset((page - 1) * page_size).limit(page_size)).all(), total

    def get(self, meeting_id: int) -> Meeting | None:
        return self.db.scalar(select(Meeting).where(Meeting.id == meeting_id).options(selectinload(Meeting.participants).selectinload(MeetingParticipant.participant), selectinload(Meeting.summary), selectinload(Meeting.topics)))

    def create(self, meeting: Meeting) -> Meeting:
        self.db.add(meeting); self.db.flush(); return meeting

    def delete(self, meeting: Meeting) -> None: self.db.delete(meeting)

    def segments(self, meeting_id: int, query: str | None = None):
        statement = select(TranscriptSegment).where(TranscriptSegment.meeting_id == meeting_id)
        if query: statement = statement.where(TranscriptSegment.content.ilike(f"%{query}%"))
        return self.db.scalars(statement.order_by(TranscriptSegment.start_time_ms)).all()

    def participant_by_name(self, name: str) -> Participant | None:
        return self.db.scalar(select(Participant).where(func.lower(Participant.display_name) == name.strip().lower()))
