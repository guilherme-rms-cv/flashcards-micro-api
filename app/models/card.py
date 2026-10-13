"""Card schemas for the flashcards API."""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

CardSource = Literal["manual", "llm"]


class CardCreate(BaseModel):
    """Input model for creating a card."""

    model_config = ConfigDict(extra="forbid")

    front: str = Field(..., min_length=1, max_length=1000)
    back: str = Field(..., min_length=1, max_length=1000)
    language: str = Field(..., min_length=2, max_length=10)
    source: CardSource
    deck_id: Optional[UUID] = None

    @field_validator("front", "back")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be empty")
        return cleaned

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if not cleaned:
            raise ValueError("language cannot be empty")
        return cleaned


class CardUpdate(BaseModel):
    """Input model for partial card updates."""

    model_config = ConfigDict(extra="forbid")

    front: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    back: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    language: Optional[str] = Field(default=None, min_length=2, max_length=10)
    source: Optional[CardSource] = None

    @field_validator("front", "back")
    @classmethod
    def validate_optional_text_fields(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be empty")
        return cleaned

    @field_validator("language")
    @classmethod
    def validate_optional_language(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        cleaned = value.strip().lower()
        if not cleaned:
            raise ValueError("language cannot be empty")
        return cleaned


class CardOut(BaseModel):
    """Card returned by the API."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: UUID
    deck_id: UUID
    front: str
    back: str
    language: str
    source: CardSource
    created_at: datetime
    updated_at: datetime


class CardBulkCreate(BaseModel):
    """Input model for creating cards in bulk."""

    model_config = ConfigDict(extra="forbid")

    cards: list[CardCreate] = Field(..., min_length=1)
    deck_id: Optional[UUID] = None
