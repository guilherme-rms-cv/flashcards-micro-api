from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.api import card_routes, deck_routes
from app.main import app
from app.repositories.card_repository import CardRepository
from app.repositories.deck_repository import DeckRepository
from app.services.card_service import CardService
from app.services.deck_service import DeckService


def test_delete_deck_removes_related_cards_with_cascade(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_delete_deck_cascade.db"
    deck_repository = DeckRepository(database_path=temp_db_path)
    card_repository = CardRepository(database_path=temp_db_path)

    deck_routes.service = DeckService(repository=deck_repository)
    card_routes.service = CardService(
        repository=card_repository,
        deck_repository=deck_repository,
    )

    client = TestClient(app)

    create_deck_response = client.post(
        "/decks",
        json={"name": "Deck com cascade", "description": "Teste de integridade"},
    )
    assert create_deck_response.status_code == 201
    deck_id = create_deck_response.json()["id"]

    first_card_response = client.post(
        "/cards",
        json={
            "front": "First sentence",
            "back": "Primeira frase",
            "language": "en",
            "source": "manual",
            "deck_id": deck_id,
        },
    )
    assert first_card_response.status_code == 201

    second_card_response = client.post(
        "/cards",
        json={
            "front": "Second sentence",
            "back": "Segunda frase",
            "language": "en",
            "source": "llm",
            "deck_id": deck_id,
        },
    )
    assert second_card_response.status_code == 201

    list_before_delete = client.get("/cards")
    assert list_before_delete.status_code == 200
    cards_before_delete = list_before_delete.json()
    assert len(cards_before_delete) == 2

    delete_response = client.delete(f"/decks/{deck_id}")
    assert delete_response.status_code == 204

    list_after_delete = client.get("/cards")
    assert list_after_delete.status_code == 200
    assert list_after_delete.json() == []
