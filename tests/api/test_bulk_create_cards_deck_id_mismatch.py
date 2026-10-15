from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import card_routes
from app.main import app
from app.repositories.card_repository import CardRepository
from app.services.card_service import CardService


def test_bulk_create_cards_rejects_root_deck_id_in_body(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_cards_bulk_mismatch_root.db"
    isolated_repository = CardRepository(database_path=temp_db_path)
    card_routes.service = CardService(repository=isolated_repository)

    client = TestClient(app)
    path_deck_id = uuid4()

    payload = {
        "deck_id": str(uuid4()),
        "cards": [
            {
                "front": "Hello world",
                "back": "Olá mundo",
                "source": "llm",
            }
        ],
    }

    response = client.post(f"/decks/{path_deck_id}/cards/bulk", json=payload)

    assert response.status_code == 422


def test_bulk_create_cards_rejects_item_deck_id_in_body(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_cards_bulk_mismatch_item.db"
    isolated_repository = CardRepository(database_path=temp_db_path)
    card_routes.service = CardService(repository=isolated_repository)

    client = TestClient(app)
    path_deck_id = uuid4()

    payload = {
        "cards": [
            {
                "front": "Another sentence",
                "back": "Outra frase",
                "source": "manual",
                "deck_id": str(uuid4()),
            }
        ],
    }

    response = client.post(f"/decks/{path_deck_id}/cards/bulk", json=payload)

    assert response.status_code == 422
