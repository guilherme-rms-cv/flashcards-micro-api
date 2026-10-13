"""Business logic for card operations."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from app.models.card import CardBulkCreate, CardCreate, CardOut, CardUpdate
from app.repositories.card_repository import CardRepository
from app.repositories.deck_repository import DeckRepository


class CardNotFoundError(LookupError):
    """Raised when a card does not exist."""


class CardDeckNotFoundError(LookupError):
    """Raised when a related deck does not exist."""


class CardService:
    """Service layer for card CRUD operations."""

    def __init__(
        self,
        repository: CardRepository | None = None,
        deck_repository: DeckRepository | None = None,
    ) -> None:
        self.repository = repository or CardRepository()
        self.deck_repository = deck_repository or DeckRepository(
            database_path=self.repository.database_path
        )

    def create_card(self, payload: CardCreate, deck_id: str | UUID | None = None) -> CardOut:
        """Create a card and return the persisted model."""
        resolved_deck_id = self._resolve_deck_id(payload=payload, deck_id=deck_id)
        self._ensure_deck_exists(resolved_deck_id)
        row = self.repository.create(
            deck_id=resolved_deck_id,
            front=payload.front,
            back=payload.back,
            language=payload.language,
            source=payload.source,
        )
        return self._to_output(row)

    def list_cards(self, deck_id: str | UUID | None = None) -> list[CardOut]:
        """List cards, optionally filtered by deck."""
        rows = self.repository.list(deck_id=deck_id)
        return [self._to_output(row) for row in rows]

    def create_cards_bulk(
        self,
        deck_id: str | UUID,
        payload: CardBulkCreate,
    ) -> list[CardOut]:
        """Create many cards in one transaction."""
        target_deck_id = str(deck_id)
        if payload.deck_id is not None and str(payload.deck_id) != target_deck_id:
            raise ValueError("deck_id in payload must match deck_id in path")
        self._ensure_deck_exists(target_deck_id)

        prepared_cards: list[dict[str, str]] = []
        for card in payload.cards:
            if card.deck_id is not None and str(card.deck_id) != target_deck_id:
                raise ValueError("deck_id in card payload must match deck_id in path")
            prepared_cards.append(
                {
                    "front": card.front,
                    "back": card.back,
                    "language": card.language,
                    "source": card.source,
                }
            )

        rows = self.repository.bulk_create(deck_id=target_deck_id, cards=prepared_cards)
        return [self._to_output(row) for row in rows]

    def get_card_by_id(self, card_id: str | UUID) -> CardOut:
        """Return one card by identifier."""
        row = self.repository.get_by_id(card_id)
        if row is None:
            self._raise_not_found(card_id)
        return self._to_output(row)

    def update_card(self, card_id: str | UUID, payload: CardUpdate) -> CardOut:
        """Update card data and return the persisted card."""
        self._validate_update_payload(payload)
        row = self.repository.update(
            card_id=card_id,
            front=payload.front,
            back=payload.back,
            language=payload.language,
            source=payload.source,
        )
        if row is None:
            self._raise_not_found(card_id)
        return self._to_output(row)

    def delete_card(self, card_id: str | UUID) -> None:
        """Delete a card if it exists."""
        deleted = self.repository.delete(card_id)
        if not deleted:
            self._raise_not_found(card_id)

    def _resolve_deck_id(self, payload: CardCreate, deck_id: str | UUID | None) -> str:
        """Resolve deck identifier from payload or method argument."""
        chosen_deck_id = deck_id or payload.deck_id
        if chosen_deck_id is None:
            raise ValueError("deck_id is required to create a card")
        return str(chosen_deck_id)

    def _validate_update_payload(self, payload: CardUpdate) -> None:
        """Ensure update request has at least one field."""
        if (
            payload.front is None
            and payload.back is None
            and payload.language is None
            and payload.source is None
        ):
            raise ValueError("at least one field must be provided for card update")

    def _ensure_deck_exists(self, deck_id: str | UUID) -> None:
        """Validate that the target deck exists."""
        if self.deck_repository.get_by_id(deck_id) is None:
            raise CardDeckNotFoundError(f"Deck '{deck_id}' not found.")

    def _raise_not_found(self, card_id: str | UUID) -> None:
        """Raise a standardized not-found error."""
        raise CardNotFoundError(f"Card '{card_id}' not found.")

    def _to_output(self, row: dict[str, Any]) -> CardOut:
        """Convert repository data to the public card model."""
        return CardOut(
            id=UUID(str(row["id"])),
            deck_id=UUID(str(row["deck_id"])),
            front=str(row["front"]),
            back=str(row["back"]),
            language=str(row["language"]),
            source=str(row["source"]),
            created_at=datetime.fromisoformat(str(row["created_at"])),
            updated_at=datetime.fromisoformat(str(row["updated_at"])),
        )
