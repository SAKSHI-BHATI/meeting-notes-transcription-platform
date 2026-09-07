# Recall — Meeting Intelligence Platform

Recall is an original Fireflies-inspired, full-stack meeting workspace built for the Scaler SDE assignment. It ships with an immediately usable seeded library, interactive transcript playback, structured notes, action items, persistence, and API documentation.

## Live Demo

- [Open the deployed meeting workspace](https://meeting-notes-transcription-platform-o1sgevxkt-coders-58f9.vercel.app/meetings/1)
- [Open the deployed frontend home page](https://meeting-notes-transcription-platform-o1sgevxkt-coders-58f9.vercel.app/)

## GitHub Repository

[SAKSHI-BHATI/meeting-notes-transcription-platform](https://github.com/SAKSHI-BHATI/meeting-notes-transcription-platform)

## Features

- Seeded, searchable meeting library with participant filtering, sorting, and pagination.
- Interactive timestamped transcript with speaker labels, text highlighting, and player synchronization.
- Structured AI-style notes: overview, key points, decisions, topics, and action items.
- Persistent meeting and action-item CRUD backed by SQLite.
- TXT, VTT, and JSON transcript ingestion with server-side validation.

## Requirements analysis

**Must have:** meeting library/search/sort, detail workspace, two-way transcript/player syncing, transcript search/highlights, summaries/topics/decisions, meeting and action-item CRUD, SQLite persistence, seeded data. **Should have:** parser uploads, validation, pagination, responsive UI, tests and docs. **Nice to have:** global search, export, real LLM integration. **Out of scope:** real speech-to-text, live meeting bot, real authentication.

## User journeys

`Dashboard → search/sort → open meeting → read notes → search transcript → click timestamp → complete action item`

`Create meeting → paste transcript → parser normalizes segments → transactional persistence → display workspace`

## Run locally

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000`; API documentation is at `http://localhost:8000/docs`.

## Architecture and data

The project uses a modular monolith: Next.js → FastAPI routes → services → repositories → SQLAlchemy → SQLite. See [architecture](docs/architecture.md), [database](docs/database.md), [API](docs/api.md), [scaling](docs/scaling.md), [decisions](docs/decisions.md), and [interview preparation](docs/interview-prep.md).

## Database and API

The normalized SQLite schema separates meetings, participants, transcript segments, summaries, topics, and action items. Full schema rationale and the ER diagram are in [database documentation](docs/database.md). The versioned REST API is documented in [API documentation](docs/api.md); interactive OpenAPI documentation is available locally at `/docs` when the backend is running.

## Tests

`cd backend && python -m pytest` runs parser/API coverage. `cd frontend && npm run lint && npm run typecheck && npm run build` validates the client.

## Deployment

The frontend is deployed on Vercel at the [Live Demo](#live-demo) URL above. The backend is designed for deployment to Render/Railway with persistent disk storage for SQLite, `DATABASE_URL`, and `CORS_ORIGINS` set to the frontend origin. Configure `NEXT_PUBLIC_API_URL` in the frontend deployment with that backend API URL. For multi-instance production, migrate to PostgreSQL as described in the scaling guide.

## Assumptions and out of scope

The project uses a default/mock user and seeded or uploaded transcripts. Real-time meeting bots, real speech-to-text, third-party integrations, and production authentication are intentionally outside the assignment scope.
