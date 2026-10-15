from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.api import card_routes
from app.main import app
from app.repositories.card_repository import CardRepository
from app.services.card_service import CardService


def test_post_cards_without_deck_id_returns_400_and_business_error_message(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_cards_without_deck_id.db"
    isolated_repository = CardRepository(database_path=temp_db_path)
    card_routes.service = CardService(repository=isolated_repository)

    client = TestClient(app)

    payload = {
        "front": "I am building an API.",
        "back": "Eu estou construindo uma API.",
        "source": "manual",
    }

    response = client.post("/cards", json=payload)

    assert response.status_code == 400
    assert response.json() == {"detail": "deck_id is required to create a card"}
