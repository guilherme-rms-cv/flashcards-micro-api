from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import deck_routes
from app.main import app
from app.repositories.deck_repository import DeckRepository
from app.services.deck_service import DeckService


def test_get_deck_by_id_returns_404_when_deck_does_not_exist(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_decks_not_found.db"
    isolated_repository = DeckRepository(database_path=temp_db_path)
    deck_routes.service = DeckService(repository=isolated_repository)

    client = TestClient(app)
    missing_deck_id = uuid4()

    response = client.get(f"/decks/{missing_deck_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": f"Deck '{missing_deck_id}' not found."}
