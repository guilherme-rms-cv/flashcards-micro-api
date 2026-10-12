"""Business logic for deck operations."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from app.models.deck import DeckCreate, DeckOut, DeckUpdate
from app.repositories.deck_repository import DeckRepository


class DeckNotFoundError(LookupError):
    """Raised when a deck does not exist."""


class DeckService:
    """Service layer for deck CRUD operations."""

    def __init__(self, repository: DeckRepository | None = None) -> None:
        self.repository = repository or DeckRepository()

    def create_deck(self, payload: DeckCreate) -> DeckOut:
        """Create a deck and return the persisted model."""
        data = self.repository.create(
            name=payload.name,
            description=payload.description,
        )
        return self._to_output(data)

    def list_decks(self) -> list[DeckOut]:
        """Return all decks in the repository."""
        rows = self.repository.list()
        return [self._to_output(row) for row in rows]

    def get_deck_by_id(self, deck_id: str | UUID) -> DeckOut:
        """Return one deck by identifier."""
        row = self.repository.get_by_id(deck_id)
        if row is None:
            raise DeckNotFoundError(f"Deck '{deck_id}' not found.")
        return self._to_output(row)

    def update_deck(self, deck_id: str | UUID, payload: DeckUpdate) -> DeckOut:
        """Update deck data and return the persisted deck."""
        existing = self.repository.get_by_id(deck_id)
        if existing is None:
            raise DeckNotFoundError(f"Deck '{deck_id}' not found.")

        updated = self.repository.update(
            deck_id=deck_id,
            name=payload.name,
            description=payload.description,
        )
        if updated is None:
            raise DeckNotFoundError(f"Deck '{deck_id}' not found.")

        return self._to_output(updated)

    def delete_deck(self, deck_id: str | UUID) -> None:
        """Delete a deck if it exists."""
        existing = self.repository.get_by_id(deck_id)
        if existing is None:
            raise DeckNotFoundError(f"Deck '{deck_id}' not found.")

        deleted = self.repository.delete(deck_id)
        if not deleted:
            raise DeckNotFoundError(f"Deck '{deck_id}' not found.")

    def _to_output(self, row: dict[str, str | None]) -> DeckOut:
        """Convert repository data to the public deck model."""
        return DeckOut(
            id=UUID(str(row["id"])),
            name=str(row["name"]),
            description=row.get("description"),
            created_at=datetime.fromisoformat(str(row["created_at"])),
            updated_at=datetime.fromisoformat(str(row["updated_at"])),
        )
