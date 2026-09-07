from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.action_item import ActionItemCreate, ActionItemUpdate
from app.services.action_item_service import ActionItemService
from app.services.meeting_service import MeetingService

router = APIRouter(tags=["action-items"])
def serialize(item): return {"id":item.id,"meeting_id":item.meeting_id,"title":item.title,"description":item.description,"assignee_id":item.assignee_id,"assignee_name":item.assignee.display_name if item.assignee else None,"due_date":item.due_date,"priority":item.priority,"status":item.status,"created_at":item.created_at,"updated_at":item.updated_at}

@router.get("/meetings/{meeting_id}/action-items")
def list_items(meeting_id: int, db: Session = Depends(get_db)):
    try: MeetingService(db).get_or_raise(meeting_id)
    except LookupError as e: raise HTTPException(404, detail={"code":"not_found","message":str(e)})
    return [serialize(item) for item in ActionItemService(db).list(meeting_id)]

@router.post("/meetings/{meeting_id}/action-items", status_code=201)
def create_item(meeting_id: int, payload: ActionItemCreate, db: Session = Depends(get_db)):
    try: MeetingService(db).get_or_raise(meeting_id)
    except LookupError as e: raise HTTPException(404, detail={"code":"not_found","message":str(e)})
    return serialize(ActionItemService(db).create(meeting_id, payload))

@router.patch("/action-items/{item_id}")
def update_item(item_id: int, payload: ActionItemUpdate, db: Session = Depends(get_db)):
    try: return serialize(ActionItemService(db).update(item_id, payload))
    except LookupError as e: raise HTTPException(404, detail={"code":"not_found","message":str(e)})

@router.delete("/action-items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    try: ActionItemService(db).delete(item_id)
    except LookupError as e: raise HTTPException(404, detail={"code":"not_found","message":str(e)})
