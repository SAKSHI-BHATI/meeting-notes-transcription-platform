from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import action_items, meetings, search
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.services.meeting_service import seed_demo_data
import app.models  # registers metadata

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed_demo_data(db)
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", openapi_url="/api/v1/openapi.json", docs_url="/docs", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(meetings.router, prefix="/api/v1")
app.include_router(action_items.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")

@app.exception_handler(HTTPException)
async def http_error_handler(_: Request, exc: HTTPException):
    detail = exc.detail if isinstance(exc.detail, dict) else {}
    message = detail.get("message") or (exc.detail if isinstance(exc.detail, str) else "Request could not be completed.")
    code = detail.get("code") or "request_failed"
    return JSONResponse(status_code=exc.status_code, content={"error": {"code": code.upper(), "message": message, "details": None}})


@app.exception_handler(RequestValidationError)
async def validation_error_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(status_code=422, content={"error": {"code": "VALIDATION_ERROR", "message": "Request validation failed.", "details": exc.errors()}})

@app.get("/health")
def health(): return {"status":"ok", "environment":settings.app_env}
