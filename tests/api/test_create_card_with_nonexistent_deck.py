from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import card_routes
from app.main import app
from app.repositories.card_repository import CardRepository
from app.repositories.deck_repository import DeckRepository
from app.services.card_service import CardService


def test_post_cards_with_nonexistent_deck_id_returns_404(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_cards_nonexistent_deck.db"
    isolated_card_repository = CardRepository(database_path=temp_db_path)
    isolated_deck_repository = DeckRepository(database_path=temp_db_path)
    card_routes.service = CardService(
        repository=isolated_card_repository,
        deck_repository=isolated_deck_repository,
    )

    client = TestClient(app)
    fake_deck_id = uuid4()

    payload = {
        "front": "I am building an API.",
        "back": "Eu estou construindo uma API.",
        "language": "en",
        "source": "manual",
        "deck_id": str(fake_deck_id),
    }

    response = client.post("/cards", json=payload)

    assert response.status_code == 404
    assert response.json() == {"detail": f"Deck '{fake_deck_id}' not found."}
