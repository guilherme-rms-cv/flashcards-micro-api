from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.api import deck_routes
from app.main import app
from app.repositories.deck_repository import DeckRepository
from app.services.deck_service import DeckService


def test_delete_deck_returns_204_and_deck_is_not_found_afterwards(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_decks_delete.db"
    isolated_repository = DeckRepository(database_path=temp_db_path)
    deck_routes.service = DeckService(repository=isolated_repository)

    client = TestClient(app)

    create_response = client.post(
        "/decks",
        json={
            "name": "Deck para Remocao",
            "description": "Deck que sera excluido no teste.",
        },
    )
    assert create_response.status_code == 201
    deck_id = create_response.json()["id"]

    delete_response = client.delete(f"/decks/{deck_id}")
    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(f"/decks/{deck_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": f"Deck '{deck_id}' not found."}
