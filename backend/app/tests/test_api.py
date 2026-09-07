import os
os.environ["DATABASE_URL"] = "sqlite:///./test_meeting_intelligence.db"
from fastapi.testclient import TestClient
from app.main import app

def test_health_and_seeded_meetings():
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        response = client.get("/api/v1/meetings")
        assert response.status_code == 200
        assert response.json()["total"] >= 8

def test_create_and_complete_action_item():
    with TestClient(app) as client:
        meeting_id = client.get("/api/v1/meetings").json()["items"][0]["id"]
        item = client.post(f"/api/v1/meetings/{meeting_id}/action-items", json={"title":"Send brief", "priority":"high"}).json()
        assert item["status"] == "open"
        updated = client.patch(f"/api/v1/action-items/{item['id']}", json={"status":"completed"}).json()
        assert updated["status"] == "completed"


def test_meeting_crud_search_filter_and_error_shape():
    with TestClient(app) as client:
        created = client.post("/api/v1/meetings", json={"title":"Launch review", "occurred_at":"2026-09-07T10:00:00", "duration_ms":120_000, "participant_names":["Maya Patel"], "transcript_text":"[00:00] Maya: Launch is ready."})
        assert created.status_code == 201
        meeting_id = created.json()["id"]
        assert client.get("/api/v1/meetings", params={"q":"Launch review"}).json()["total"] == 1
        assert client.get("/api/v1/meetings", params={"participant":"Maya Patel"}).status_code == 200
        assert client.patch(f"/api/v1/meetings/{meeting_id}", json={"title":"Launch review updated"}).json()["title"] == "Launch review updated"
        assert client.delete(f"/api/v1/meetings/{meeting_id}").status_code == 204
        missing = client.get(f"/api/v1/meetings/{meeting_id}")
        assert missing.status_code == 404
        assert missing.json()["error"]["code"] == "NOT_FOUND"


def test_transcript_search_and_upload_validation():
    with TestClient(app) as client:
        meeting_id = client.get("/api/v1/meetings").json()["items"][0]["id"]
        search = client.get(f"/api/v1/meetings/{meeting_id}/transcript/search", params={"q":"launch"})
        assert search.status_code == 200
        assert search.json()["items"]
        invalid = client.post(f"/api/v1/meetings/{meeting_id}/transcript/upload", files={"file": ("notes.pdf", b"not a transcript", "application/pdf")})
        assert invalid.status_code == 415
        assert invalid.json()["error"]["code"] == "INVALID_FILE"
