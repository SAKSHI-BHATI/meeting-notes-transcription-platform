# API overview

All application endpoints are under `/api/v1` and return JSON. Errors use the consistent envelope `{ "error": { "code": "VALIDATION_ERROR", "message": "…", "details": [] } }`; validation errors use HTTP 422 and missing records use HTTP 404.

| Method | Endpoint | Purpose |
|---|---|---|
| GET/POST | `/meetings` | Paginated, searchable meeting library / creation |
| GET | `/search?q=` | Global search across meeting titles, participants, and transcript text |
| GET/PATCH/DELETE | `/meetings/{id}` | Meeting retrieval and metadata CRUD |
| GET | `/meetings/{id}/transcript?q=` | Ordered transcript, optionally filtered by text |
| GET | `/meetings/{id}/transcript/search?q=` | Transcript search results for an explicit query |
| POST | `/meetings/{id}/transcript/upload` | Parse TXT, VTT, or JSON (2 MB limit) |
| GET | `/meetings/{id}/summary`, `/topics` | Structured intelligence |
| GET/POST | `/meetings/{id}/action-items` | Action-item collection |
| PATCH/DELETE | `/action-items/{id}` | Update, complete/reopen, delete |

`GET /meetings` accepts `q`, `participant`, `date_from`, `date_to`, `sort=recent|oldest|title`, `page`, and `page_size`. Date values use ISO calendar dates (`YYYY-MM-DD`); `date_from` is inclusive and `date_to` includes the full calendar day.
