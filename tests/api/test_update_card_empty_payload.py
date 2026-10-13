from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from app.api import card_routes
from app.main import app
from app.repositories.card_repository import CardRepository
from app.services.card_service import CardService


def test_put_card_with_empty_payload_returns_400_and_validation_message(tmp_path: Path) -> None:
    temp_db_path = tmp_path / "test_cards_update_empty_payload.db"
    isolated_repository = CardRepository(database_path=temp_db_path)
    card_routes.service = CardService(repository=isolated_repository)

    client = TestClient(app)
    missing_card_id = uuid4()

    response = client.put(f"/cards/{missing_card_id}", json={})

    assert response.status_code == 400
    assert response.json() == {"detail": "at least one field must be provided for card update"}
