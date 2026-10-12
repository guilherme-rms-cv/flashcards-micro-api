"""SQLite repository for deck persistence."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from uuid import UUID, uuid4

DECK_COLUMNS = "id, name, description, created_at, updated_at"
SELECT_DECK_BASE = f"SELECT {DECK_COLUMNS} FROM decks"


class DeckRepository:
    """Repository for CRUD operations on decks."""

    def __init__(self, database_path: str | Path = "data/decks.db") -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @staticmethod
    def _normalize_deck_id(deck_id: str | UUID) -> str:
        return str(deck_id)

    @staticmethod
    def _row_to_dict(row: sqlite3.Row | None) -> Optional[dict[str, Any]]:
        return None if row is None else dict(row)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS decks (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def create(self, name: str, description: Optional[str] = None) -> dict[str, Any]:
        """Create a new deck."""
        deck_id = str(uuid4())
        created_at = self._utc_now()
        payload = {
            "id": deck_id,
            "name": name.strip(),
            "description": description.strip() if description else None,
            "created_at": created_at,
            "updated_at": created_at,
        }

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO decks (id, name, description, created_at, updated_at)
                VALUES (:id, :name, :description, :created_at, :updated_at)
                """,
                payload,
            )

        return payload

    def list(self) -> list[dict[str, Any]]:
        """Return all decks ordered by creation time."""
        with self._connect() as connection:
            rows = connection.execute(
                f"{SELECT_DECK_BASE} ORDER BY created_at ASC"
            ).fetchall()

        return [dict(row) for row in rows]

    def get_by_id(self, deck_id: str | UUID) -> Optional[dict[str, Any]]:
        """Return a single deck by identifier, if present."""
        target_id = self._normalize_deck_id(deck_id)
        with self._connect() as connection:
            row = connection.execute(
                f"{SELECT_DECK_BASE} WHERE id = ?",
                (target_id,),
            ).fetchone()

        return self._row_to_dict(row)

    def update(
        self,
        deck_id: str | UUID,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        """Update a deck by identifier."""
        current = self.get_by_id(deck_id)
        if current is None:
            return None

        updated_name = name.strip() if name is not None else current["name"]
        updated_description = description.strip() if description is not None else current["description"]
        updated_at = self._utc_now()

        payload = {
            "id": self._normalize_deck_id(deck_id),
            "name": updated_name,
            "description": updated_description,
            "updated_at": updated_at,
        }

        with self._connect() as connection:
            connection.execute(
                """
                UPDATE decks
                SET name = :name,
                    description = :description,
                    updated_at = :updated_at
                WHERE id = :id
                """,
                payload,
            )

        result = self.get_by_id(payload["id"])
        return result

    def delete(self, deck_id: str | UUID) -> bool:
        """Delete a deck by identifier."""
        target_id = self._normalize_deck_id(deck_id)
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM decks WHERE id = ?", (target_id,))
        return cursor.rowcount > 0
