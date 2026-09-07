# Architecture

Recall is a modular monolith: a Next.js client calls a versioned FastAPI REST API, whose routers delegate to services and repositories backed by SQLite/SQLAlchemy. This keeps local deployment and interview comprehension simple while retaining replaceable boundaries.

```mermaid
flowchart LR
 Browser --> Next[Next.js TypeScript]
 Next --> API[FastAPI /api/v1]
 API --> Service[Service layer]
 Service --> Repository[Repository layer]
 Repository --> ORM[SQLAlchemy]
 ORM --> DB[(SQLite)]
```

Routes validate HTTP contracts; services own transactions and business workflows; repositories own query composition. The frontend keeps requests in `services/api.ts`, cached with TanStack Query.
