"""SQLite repository for card persistence."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from uuid import UUID, uuid4

CARD_COLUMNS = "id, deck_id, front, back, language, source, created_at, updated_at"
SELECT_CARD_BASE = f"SELECT {CARD_COLUMNS} FROM cards"


class CardRepository:
    """Repository for CRUD operations on cards."""

    def __init__(self, database_path: str | Path = "data/decks.db") -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @staticmethod
    def _normalize_id(value: str | UUID) -> str:
        return str(value)

    @staticmethod
    def _row_to_dict(row: sqlite3.Row | None) -> Optional[dict[str, Any]]:
        return None if row is None else dict(row)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            self._ensure_decks_table(connection)
            self._ensure_cards_table_with_cascade(connection)
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_cards_deck_id ON cards(deck_id)"
            )

    def _ensure_decks_table(self, connection: sqlite3.Connection) -> None:
        """Ensure deck table exists for foreign key reference."""
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

    def _ensure_cards_table_with_cascade(self, connection: sqlite3.Connection) -> None:
        """Ensure cards table has ON DELETE CASCADE foreign key."""
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS cards (
                id TEXT PRIMARY KEY,
                deck_id TEXT NOT NULL,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                language TEXT NOT NULL,
                source TEXT NOT NULL CHECK(source IN ('manual', 'llm')),
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(deck_id) REFERENCES decks(id) ON DELETE CASCADE
            )
            """
        )

        if self._cards_table_has_cascade_fk(connection):
            return

        self._migrate_cards_table_to_cascade(connection)

    def _cards_table_has_cascade_fk(self, connection: sqlite3.Connection) -> bool:
        """Check if cards table has cascade foreign key to decks."""
        rows = connection.execute("PRAGMA foreign_key_list(cards)").fetchall()
        for row in rows:
            target_table = str(row["table"]).lower()
            from_column = str(row["from"]).lower()
            on_delete = str(row["on_delete"]).upper()
            if target_table == "decks" and from_column == "deck_id" and on_delete == "CASCADE":
                return True
        return False

    def _migrate_cards_table_to_cascade(self, connection: sqlite3.Connection) -> None:
        """Recreate cards table with cascade delete and preserve valid rows."""
        connection.execute(
            """
            CREATE TABLE cards_new (
                id TEXT PRIMARY KEY,
                deck_id TEXT NOT NULL,
                front TEXT NOT NULL,
                back TEXT NOT NULL,
                language TEXT NOT NULL,
                source TEXT NOT NULL CHECK(source IN ('manual', 'llm')),
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(deck_id) REFERENCES decks(id) ON DELETE CASCADE
            )
            """
        )
        connection.execute(
            """
            INSERT INTO cards_new (id, deck_id, front, back, language, source, created_at, updated_at)
            SELECT c.id, c.deck_id, c.front, c.back, c.language, c.source, c.created_at, c.updated_at
            FROM cards c
            WHERE EXISTS (SELECT 1 FROM decks d WHERE d.id = c.deck_id)
            """
        )
        connection.execute("DROP TABLE cards")
        connection.execute("ALTER TABLE cards_new RENAME TO cards")

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def create(
        self,
        deck_id: str | UUID,
        front: str,
        back: str,
        language: str,
        source: str,
    ) -> dict[str, Any]:
        """Create a new card."""
        card_id = str(uuid4())
        timestamp = self._utc_now()
        payload = {
            "id": card_id,
            "deck_id": self._normalize_id(deck_id),
            "front": front.strip(),
            "back": back.strip(),
            "language": language.strip().lower(),
            "source": source.strip().lower(),
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO cards (id, deck_id, front, back, language, source, created_at, updated_at)
                VALUES (:id, :deck_id, :front, :back, :language, :source, :created_at, :updated_at)
                """,
                payload,
            )

        return payload

    def bulk_create(
        self,
        deck_id: str | UUID,
        cards: list[dict[str, str]],
    ) -> list[dict[str, Any]]:
        """Create many cards in one transaction."""
        target_deck_id = self._normalize_id(deck_id)
        rows: list[dict[str, Any]] = []
        timestamp = self._utc_now()

        for card in cards:
            rows.append(
                {
                    "id": str(uuid4()),
                    "deck_id": target_deck_id,
                    "front": card["front"].strip(),
                    "back": card["back"].strip(),
                    "language": card["language"].strip().lower(),
                    "source": card["source"].strip().lower(),
                    "created_at": timestamp,
                    "updated_at": timestamp,
                }
            )

        with self._connect() as connection:
            connection.executemany(
                """
                INSERT INTO cards (id, deck_id, front, back, language, source, created_at, updated_at)
                VALUES (:id, :deck_id, :front, :back, :language, :source, :created_at, :updated_at)
                """,
                rows,
            )

        return rows

    def list(self, deck_id: str | UUID | None = None) -> list[dict[str, Any]]:
        """Return all cards, optionally filtered by deck."""
        query = f"{SELECT_CARD_BASE} ORDER BY created_at ASC"
        params: tuple[str, ...] = ()
        if deck_id is not None:
            query = f"{SELECT_CARD_BASE} WHERE deck_id = ? ORDER BY created_at ASC"
            params = (self._normalize_id(deck_id),)

        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()

        return [dict(row) for row in rows]

    def get_by_id(self, card_id: str | UUID) -> Optional[dict[str, Any]]:
        """Return one card by identifier, if present."""
        target_id = self._normalize_id(card_id)
        with self._connect() as connection:
            row = connection.execute(
                f"{SELECT_CARD_BASE} WHERE id = ?",
                (target_id,),
            ).fetchone()

        return self._row_to_dict(row)

    def update(
        self,
        card_id: str | UUID,
        front: Optional[str] = None,
        back: Optional[str] = None,
        language: Optional[str] = None,
        source: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        """Update a card by identifier."""
        current = self.get_by_id(card_id)
        if current is None:
            return None

        payload = {
            "id": self._normalize_id(card_id),
            "front": front.strip() if front is not None else current["front"],
            "back": back.strip() if back is not None else current["back"],
            "language": language.strip().lower() if language is not None else current["language"],
            "source": source.strip().lower() if source is not None else current["source"],
            "updated_at": self._utc_now(),
        }

        with self._connect() as connection:
            connection.execute(
                """
                UPDATE cards
                SET front = :front,
                    back = :back,
                    language = :language,
                    source = :source,
                    updated_at = :updated_at
                WHERE id = :id
                """,
                payload,
            )

        return self.get_by_id(payload["id"])

    def delete(self, card_id: str | UUID) -> bool:
        """Delete a card by identifier."""
        target_id = self._normalize_id(card_id)
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM cards WHERE id = ?", (target_id,))
        return cursor.rowcount > 0
