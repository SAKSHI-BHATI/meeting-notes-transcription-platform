from sqlalchemy.orm import Session
from app.models import ActionItem
from app.repositories.action_item_repository import ActionItemRepository
from app.schemas.action_item import ActionItemCreate, ActionItemUpdate


class ActionItemService:
    def __init__(self, db: Session): self.db, self.repo = db, ActionItemRepository(db)
    def list(self, meeting_id: int): return self.repo.list_for_meeting(meeting_id)
    def create(self, meeting_id: int, payload: ActionItemCreate):
        item = self.repo.create(ActionItem(meeting_id=meeting_id, **payload.model_dump())); self.db.commit(); return self.repo.get(item.id)
    def update(self, item_id: int, payload: ActionItemUpdate):
        item = self.repo.get(item_id)
        if not item: raise LookupError("Action item not found")
        for key, value in payload.model_dump(exclude_unset=True).items(): setattr(item, key, value)
        self.db.commit(); return self.repo.get(item.id)
    def delete(self, item_id: int):
        item = self.repo.get(item_id)
        if not item: raise LookupError("Action item not found")
        self.repo.delete(item); self.db.commit()
