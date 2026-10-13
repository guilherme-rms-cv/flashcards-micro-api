from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import card_routes
from app.main import app
from app.repositories.card_repository import CardRepository
from app.repositories.deck_repository import DeckRepository
from app.services.card_service import CardService


def test_bulk_create_cards_returns_400_when_root_deck_id_differs_from_path(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_cards_bulk_mismatch_root.db"
    isolated_repository = CardRepository(database_path=temp_db_path)
    card_routes.service = CardService(repository=isolated_repository)

    client = TestClient(app)
    path_deck_id = uuid4()
    payload_deck_id = uuid4()

    payload = {
        "deck_id": str(payload_deck_id),
        "cards": [
            {
                "front": "Hello world",
                "back": "Olá mundo",
                "language": "en",
                "source": "llm",
            }
        ],
    }

    response = client.post(f"/decks/{path_deck_id}/cards/bulk", json=payload)

    assert response.status_code == 400
    assert response.json() == {"detail": "deck_id in payload must match deck_id in path"}


def test_bulk_create_cards_returns_400_when_card_deck_id_differs_from_path(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_cards_bulk_mismatch_item.db"
    isolated_repository = CardRepository(database_path=temp_db_path)
    deck_repository = DeckRepository(database_path=temp_db_path)
    card_routes.service = CardService(
        repository=isolated_repository,
        deck_repository=deck_repository,
    )

    client = TestClient(app)
    created_deck = deck_repository.create(name="Deck Mismatch", description="Deck para mismatch")
    path_deck_id = created_deck["id"]
    card_payload_deck_id = uuid4()

    payload = {
        "cards": [
            {
                "front": "Another sentence",
                "back": "Outra frase",
                "language": "en",
                "source": "manual",
                "deck_id": str(card_payload_deck_id),
            }
        ],
    }

    response = client.post(f"/decks/{path_deck_id}/cards/bulk", json=payload)

    assert response.status_code == 400
    assert response.json() == {"detail": "deck_id in card payload must match deck_id in path"}
