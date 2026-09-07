from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.models import ActionItem


class ActionItemRepository:
    def __init__(self, db: Session): self.db = db
    def list_for_meeting(self, meeting_id: int):
        return self.db.scalars(select(ActionItem).where(ActionItem.meeting_id == meeting_id).options(selectinload(ActionItem.assignee)).order_by(ActionItem.status, ActionItem.created_at.desc())).all()
    def get(self, item_id: int):
        return self.db.scalar(select(ActionItem).where(ActionItem.id == item_id).options(selectinload(ActionItem.assignee)))
    def create(self, item: ActionItem): self.db.add(item); self.db.flush(); return item
    def delete(self, item: ActionItem): self.db.delete(item)
