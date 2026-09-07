from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Meeting, MeetingParticipant, Participant, Summary, Topic, TranscriptSegment
from app.repositories.meeting_repository import MeetingRepository
from app.schemas.meeting import MeetingCreate, MeetingUpdate, SegmentCreate
from app.services.transcript_parser import TxtParser


class MeetingService:
    def __init__(self, db: Session): self.db, self.repo = db, MeetingRepository(db)

    def list(self, **kwargs): return self.repo.list(**kwargs)

    def get_or_raise(self, meeting_id: int) -> Meeting:
        meeting = self.repo.get(meeting_id)
        if not meeting: raise LookupError("Meeting not found")
        return meeting

    def create(self, payload: MeetingCreate) -> Meeting:
        meeting = self.repo.create(Meeting(owner_id=1, title=payload.title, occurred_at=payload.occurred_at, duration_ms=payload.duration_ms, source="pasted" if payload.transcript_text else "manual"))
        self._replace_participants(meeting, payload.participant_names)
        if payload.transcript_text: self._replace_segments(meeting, TxtParser().parse(payload.transcript_text))
        self.db.commit(); self.db.refresh(meeting)
        return meeting

    def update(self, meeting_id: int, payload: MeetingUpdate) -> Meeting:
        meeting = self.get_or_raise(meeting_id)
        for key, value in payload.model_dump(exclude_unset=True, exclude={"participant_names"}).items(): setattr(meeting, key, value)
        if payload.participant_names is not None: self._replace_participants(meeting, payload.participant_names)
        self.db.commit(); return self.get_or_raise(meeting.id)

    def delete(self, meeting_id: int):
        self.repo.delete(self.get_or_raise(meeting_id)); self.db.commit()

    def replace_uploaded_transcript(self, meeting_id: int, segments: list[SegmentCreate]):
        meeting = self.get_or_raise(meeting_id); self._replace_segments(meeting, segments)
        if segments: meeting.duration_ms = max(segment.end_time_ms for segment in segments)
        self.db.commit()

    def _replace_participants(self, meeting: Meeting, names: list[str]):
        meeting.participants.clear()
        for name in dict.fromkeys(name.strip() for name in names if name.strip()):
            participant = self.repo.participant_by_name(name)
            if not participant:
                participant = Participant(display_name=name, initials="".join(word[0].upper() for word in name.split()[:2]), color="#6D5CE7")
                self.db.add(participant); self.db.flush()
            meeting.participants.append(MeetingParticipant(participant=participant))

    def _replace_segments(self, meeting: Meeting, segments: list[SegmentCreate]):
        meeting.segments.clear(); self.db.flush()
        meeting.segments.extend(TranscriptSegment(speaker_name=s.speaker_name, start_time_ms=s.start_time_ms, end_time_ms=max(s.end_time_ms, s.start_time_ms + 1), content=s.content) for s in segments)


def seed_demo_data(db: Session):
    if db.query(Meeting).count(): return
    owner = Participant(display_name="Olivia Carter", email="olivia@recall.demo", initials="OC", color="#6D5CE7")
    db.add_all([__import__("app.models", fromlist=["User"]).User(name="Olivia Carter", email="olivia@recall.demo"), owner]); db.flush()
    people = [owner, Participant(display_name="Maya Patel", email="maya@recall.demo", initials="MP", color="#F97316"), Participant(display_name="Noah Williams", email="noah@recall.demo", initials="NW", color="#0EA5E9"), Participant(display_name="Ethan Brooks", email="ethan@recall.demo", initials="EB", color="#10B981")]
    db.add_all(people[1:]); db.flush()
    meetings = [("Weekly product sync", "2026-09-05 10:00", 2760000), ("Atlas launch retrospective", "2026-09-03 14:30", 3180000), ("Customer discovery Northstar", "2026-09-01 11:00", 2340000), ("Design critique Mobile onboarding", "2026-08-29 15:00", 2520000), ("Engineering planning Q4", "2026-08-27 09:30", 3600000), ("Growth experiment review", "2026-08-25 16:00", 1980000), ("Hiring debrief Platform", "2026-08-22 13:00", 2100000), ("Partner roadmap review", "2026-08-20 10:00", 2880000)]
    script = [("Olivia Carter", "Let’s align on the launch goals and what needs to happen this week."), ("Maya Patel", "The onboarding flow is ready for the final copy review and the analytics events are mapped."), ("Noah Williams", "Engineering can ship the remaining dashboard work by Thursday if we freeze scope today."), ("Ethan Brooks", "I’ll share the customer feedback synthesis and update the success metric baseline."), ("Olivia Carter", "Great. We will hold the release date, keep the scope focused, and review results next Monday.")]
    for idx, (title, occurred, duration) in enumerate(meetings):
        meeting = Meeting(owner_id=1, title=title, occurred_at=datetime.fromisoformat(occurred), duration_ms=duration, source="seeded")
        db.add(meeting); db.flush()
        for person in people[:3 + (idx % 2)]: db.add(MeetingParticipant(meeting_id=meeting.id, participant_id=person.id))
        for pos, (speaker, text) in enumerate(script): db.add(TranscriptSegment(meeting_id=meeting.id, speaker_name=speaker, start_time_ms=pos*45000, end_time_ms=pos*45000+39000, content=text))
        db.add(Summary(meeting_id=meeting.id, overview=f"The team reviewed {title.lower()} and aligned on a focused delivery plan with clear owners.", key_points_json='["Scope is intentionally focused", "Teams have clear delivery owners", "Success will be reviewed next week"]', decisions_json='["Maintain the agreed release date", "Defer non-critical requests"]', provider="seeded"))
        db.add_all([Topic(meeting_id=meeting.id, label="Goals and progress", start_time_ms=0), Topic(meeting_id=meeting.id, label="Delivery plan", start_time_ms=90000)])
    db.commit()
