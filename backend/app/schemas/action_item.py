from datetime import date, datetime
from pydantic import BaseModel, Field


class ActionItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=5000)
    assignee_id: int | None = None
    due_date: date | None = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")


class ActionItemUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, max_length=5000)
    assignee_id: int | None = None
    due_date: date | None = None
    priority: str | None = Field(default=None, pattern="^(low|medium|high)$")
    status: str | None = Field(default=None, pattern="^(open|completed)$")


class ActionItemRead(BaseModel):
    id: int
    meeting_id: int
    title: str
    description: str | None
    assignee_id: int | None
    assignee_name: str | None
    due_date: date | None
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime
