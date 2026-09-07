# Interview preparation

**Why modular monolith?** It has deployment simplicity without sacrificing testable boundaries. **Why FastAPI?** Typed Pydantic validation and generated OpenAPI make a small REST API clear. **Why SQLite?** It is portable and durable for a single-user assignment; PostgreSQL is the path for write concurrency.

**Why separate segments and milliseconds?** Segments can be indexed, searched, and synchronized independently; integer milliseconds match media APIs without float drift. **How does synchronization work?** On player updates, the client binary-searches the ordered segment start times and scrolls the active node into view (O(log n)).

**How would this scale?** Move to PostgreSQL, use full-text/search infrastructure for transcripts, store recordings in object storage, and send transcription/AI work to background workers. Auth would use session/JWT identity and authorization checks; uploads would keep type/size validation plus object-store scanning. Repositories centralize data access while services define transaction boundaries. TanStack Query provides cache invalidation and can support optimistic updates with rollback.
