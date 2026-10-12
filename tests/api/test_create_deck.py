from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import UUID

from fastapi.testclient import TestClient

from app.api import deck_routes
from app.main import app
from app.repositories.deck_repository import DeckRepository
from app.services.deck_service import DeckService


def test_post_decks_creates_deck_with_201_and_persists(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_decks.db"
    isolated_repository = DeckRepository(database_path=temp_db_path)
    deck_routes.service = DeckService(repository=isolated_repository)

    client = TestClient(app)

    payload = {
        "name": "English Phrases",
        "description": "Frases em inglês para revisão diária.",
    }
    response = client.post("/decks", json=payload)

    assert response.status_code == 201
    body = response.json()

    assert set(body.keys()) == {"id", "name", "description", "created_at", "updated_at"}
    UUID(body["id"])
    assert body["name"] == payload["name"]
    assert body["description"] == payload["description"]

    created_at = datetime.fromisoformat(body["created_at"])
    updated_at = datetime.fromisoformat(body["updated_at"])
    assert created_at <= updated_at

    persisted_deck = isolated_repository.get_by_id(body["id"])
    assert persisted_deck is not None
    assert persisted_deck["id"] == body["id"]
    assert persisted_deck["name"] == payload["name"]
    assert persisted_deck["description"] == payload["description"]
