from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import card_routes
from app.main import app
from app.repositories.card_repository import CardRepository
from app.services.card_service import CardService


def test_bulk_create_cards_is_all_or_nothing_when_payload_has_invalid_item(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_cards_bulk_transaction.db"
    isolated_repository = CardRepository(database_path=temp_db_path)
    card_routes.service = CardService(repository=isolated_repository)

    client = TestClient(app)
    deck_id = uuid4()

    payload = {
        "cards": [
            {
                "front": "Valid sentence",
                "back": "Frase válida",
                "language": "en",
                "source": "llm",
            },
            {
                "front": "Invalid source item",
                "back": "Item inválido por source",
                "language": "en",
                "source": "invalid-source",
            },
        ]
    }

    response = client.post(f"/decks/{deck_id}/cards/bulk", json=payload)

    assert response.status_code == 422
    persisted_cards = isolated_repository.list(deck_id=deck_id)
    assert persisted_cards == []
