from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.api import deck_routes
from app.main import app
from app.repositories.deck_repository import DeckRepository
from app.services.deck_service import DeckService


def test_update_deck_changes_only_name_and_keeps_description(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_decks_update_partial_name.db"
    isolated_repository = DeckRepository(database_path=temp_db_path)
    deck_routes.service = DeckService(repository=isolated_repository)

    client = TestClient(app)

    create_response = client.post(
        "/decks",
        json={
            "name": "Deck Inicial",
            "description": "Descricao original",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    deck_id = created["id"]

    update_response = client.put(
        f"/decks/{deck_id}",
        json={"name": "Deck Renomeado"},
    )
    assert update_response.status_code == 200
    updated = update_response.json()

    assert updated["name"] == "Deck Renomeado"
    assert updated["description"] == "Descricao original"

    get_response = client.get(f"/decks/{deck_id}")
    assert get_response.status_code == 200
    persisted = get_response.json()
    assert persisted["name"] == "Deck Renomeado"
    assert persisted["description"] == "Descricao original"


def test_update_deck_changes_only_description_and_keeps_name(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_decks_update_partial_description.db"
    isolated_repository = DeckRepository(database_path=temp_db_path)
    deck_routes.service = DeckService(repository=isolated_repository)

    client = TestClient(app)

    create_response = client.post(
        "/decks",
        json={
            "name": "Deck de Frases",
            "description": "Descricao antiga",
        },
    )
    assert create_response.status_code == 201
    created = create_response.json()
    deck_id = created["id"]

    update_response = client.put(
        f"/decks/{deck_id}",
        json={"description": "Descricao nova"},
    )
    assert update_response.status_code == 200
    updated = update_response.json()

    assert updated["name"] == "Deck de Frases"
    assert updated["description"] == "Descricao nova"

    get_response = client.get(f"/decks/{deck_id}")
    assert get_response.status_code == 200
    persisted = get_response.json()
    assert persisted["name"] == "Deck de Frases"
    assert persisted["description"] == "Descricao nova"
