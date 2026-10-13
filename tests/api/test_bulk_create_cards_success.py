from __future__ import annotations

from pathlib import Path
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.api import card_routes
from app.main import app
from app.repositories.card_repository import CardRepository
from app.services.card_service import CardService


def test_bulk_create_cards_returns_201_and_persists_all_items(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_cards_bulk_success.db"
    isolated_repository = CardRepository(database_path=temp_db_path)
    card_routes.service = CardService(repository=isolated_repository)

    client = TestClient(app)
    deck_id = uuid4()

    payload = {
        "cards": [
            {
                "front": "Another important part of my job is deploying models into production.",
                "back": "Outra parte importante do meu trabalho é a implantação de modelos em produção.",
                "language": "en",
                "source": "llm",
            },
            {
                "front": "Then, I create an inference service, usually using Python and FastAPI.",
                "back": "Então, eu crio um serviço de inferência, geralmente usando Python e FastAPI.",
                "language": "en",
                "source": "llm",
            },
        ]
    }

    response = client.post(f"/decks/{deck_id}/cards/bulk", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 2

    for item in body:
        assert set(item.keys()) == {
            "id",
            "deck_id",
            "front",
            "back",
            "language",
            "source",
            "created_at",
            "updated_at",
        }
        UUID(item["id"])
        assert item["deck_id"] == str(deck_id)
        assert item["source"] in {"manual", "llm"}

    persisted_cards = isolated_repository.list(deck_id=deck_id)
    assert len(persisted_cards) == 2
    assert {card["front"] for card in persisted_cards} == {
        payload["cards"][0]["front"],
        payload["cards"][1]["front"],
    }
