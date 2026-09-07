# Production evolution

SQLite and the modular monolith are intentional for this assignment. At scale, introduce a CDN for static Next.js assets, load-balanced FastAPI instances, PostgreSQL for concurrent writes, Redis for cache/rate limits, object storage for recordings, queues and workers for transcription/summary generation, and dedicated search for cross-transcript retrieval. Each addition addresses a measurable bottleneck rather than speculation.
