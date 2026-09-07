"""initial schema
Revision ID: 0001_initial
Revises:
"""
from alembic import op
import sqlalchemy as sa
revision="0001_initial"; down_revision=None; branch_labels=None; depends_on=None
def upgrade():
    op.create_table("users",sa.Column("id",sa.Integer,primary_key=True),sa.Column("email",sa.String(255),nullable=False,unique=True),sa.Column("name",sa.String(120),nullable=False),sa.Column("created_at",sa.DateTime,server_default=sa.func.now()),sa.Column("updated_at",sa.DateTime,server_default=sa.func.now()))
    op.create_table("meetings",sa.Column("id",sa.Integer,primary_key=True),sa.Column("owner_id",sa.Integer,sa.ForeignKey("users.id"),nullable=False),sa.Column("title",sa.String(255),nullable=False),sa.Column("occurred_at",sa.DateTime,nullable=False),sa.Column("duration_ms",sa.Integer,nullable=False,server_default="0"),sa.Column("source",sa.String(30),nullable=False),sa.Column("created_at",sa.DateTime,server_default=sa.func.now()),sa.Column("updated_at",sa.DateTime,server_default=sa.func.now()))
    op.create_table("participants",sa.Column("id",sa.Integer,primary_key=True),sa.Column("display_name",sa.String(120),nullable=False),sa.Column("email",sa.String(255),unique=True),sa.Column("initials",sa.String(4),nullable=False),sa.Column("color",sa.String(16),nullable=False))
    op.create_table("meeting_participants",sa.Column("id",sa.Integer,primary_key=True),sa.Column("meeting_id",sa.Integer,sa.ForeignKey("meetings.id",ondelete="CASCADE"),nullable=False),sa.Column("participant_id",sa.Integer,sa.ForeignKey("participants.id"),nullable=False),sa.Column("role",sa.String(30),nullable=False),sa.UniqueConstraint("meeting_id","participant_id"))
    op.create_table("transcript_segments",sa.Column("id",sa.Integer,primary_key=True),sa.Column("meeting_id",sa.Integer,sa.ForeignKey("meetings.id",ondelete="CASCADE"),nullable=False),sa.Column("speaker_id",sa.Integer,sa.ForeignKey("participants.id")),sa.Column("speaker_name",sa.String(120),nullable=False),sa.Column("start_time_ms",sa.Integer,nullable=False),sa.Column("end_time_ms",sa.Integer,nullable=False),sa.Column("content",sa.Text,nullable=False))
    op.create_table("summaries",sa.Column("meeting_id",sa.Integer,sa.ForeignKey("meetings.id",ondelete="CASCADE"),primary_key=True),sa.Column("overview",sa.Text,nullable=False),sa.Column("key_points_json",sa.Text,nullable=False),sa.Column("decisions_json",sa.Text,nullable=False),sa.Column("provider",sa.String(50),nullable=False))
    op.create_table("topics",sa.Column("id",sa.Integer,primary_key=True),sa.Column("meeting_id",sa.Integer,sa.ForeignKey("meetings.id",ondelete="CASCADE"),nullable=False),sa.Column("label",sa.String(120),nullable=False),sa.Column("start_time_ms",sa.Integer))
    op.create_table("action_items",sa.Column("id",sa.Integer,primary_key=True),sa.Column("meeting_id",sa.Integer,sa.ForeignKey("meetings.id",ondelete="CASCADE"),nullable=False),sa.Column("assignee_id",sa.Integer,sa.ForeignKey("participants.id")),sa.Column("title",sa.String(300),nullable=False),sa.Column("description",sa.Text),sa.Column("due_date",sa.Date),sa.Column("priority",sa.String(20),nullable=False),sa.Column("status",sa.String(20),nullable=False),sa.Column("created_at",sa.DateTime,server_default=sa.func.now()),sa.Column("updated_at",sa.DateTime,server_default=sa.func.now()))
    op.create_index("ix_segments_meeting_start","transcript_segments",["meeting_id","start_time_ms"]);op.create_index("ix_meetings_owner_occurred","meetings",["owner_id","occurred_at"]);op.create_index("ix_action_items_meeting_status","action_items",["meeting_id","status"])
def downgrade():
    for table in ["action_items","topics","summaries","transcript_segments","meeting_participants","participants","meetings","users"]: op.drop_table(table)
