# Database schema

`meetings` stores metadata only. Large, independently queried data lives in related tables.

```mermaid
erDiagram
 USERS ||--o{ MEETINGS : owns
 MEETINGS ||--o{ MEETING_PARTICIPANTS : includes
 PARTICIPANTS ||--o{ MEETING_PARTICIPANTS : joins
 MEETINGS ||--o{ TRANSCRIPT_SEGMENTS : contains
 MEETINGS ||--|| SUMMARIES : has
 MEETINGS ||--o{ TOPICS : has
 MEETINGS ||--o{ ACTION_ITEMS : tracks
 PARTICIPANTS ||--o{ ACTION_ITEMS : assigned
```

Important indexes: `(meeting_id, start_time_ms)` supports ordered transcript retrieval, `(owner_id, occurred_at)` supports library recency, and `(meeting_id, status)` supports action-item panels. Timestamps within transcripts are integer milliseconds to avoid floating-point seek drift.
