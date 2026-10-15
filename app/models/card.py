"""Card schemas for the flashcards API."""

from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

CardSource = Literal["manual", "llm"]


class CardCreate(BaseModel):
    """Input model for creating a card."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "front": "I review flashcards every morning.",
                "back": "Eu reviso flashcards toda manhã.",
                "source": "manual",
                "deck_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            }
        },
    )

    front: str = Field(..., min_length=1, max_length=1000)
    back: str = Field(..., min_length=1, max_length=1000)
    source: CardSource
    deck_id: Optional[UUID] = None

    @field_validator("front", "back")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be empty")
        return cleaned


class CardBulkItemCreate(BaseModel):
    """Input model for one bulk card item."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "front": "Then, I create an inference service using FastAPI.",
                "back": "Então, eu crio um serviço de inferência usando FastAPI.",
                "source": "llm",
            }
        },
    )

    front: str = Field(..., min_length=1, max_length=1000)
    back: str = Field(..., min_length=1, max_length=1000)
    source: CardSource

    @field_validator("front", "back")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be empty")
        return cleaned


class CardUpdate(BaseModel):
    """Input model for partial card updates."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "front": "Monitoring in production prevents silent failures.",
                "source": "manual",
            }
        },
    )

    front: Optional[str] = Field(default=None, min_length=1, max_length=1000)
    back: Optional[str] = Field(default=None, min_length=1, max_length=1000)
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


class CardOut(BaseModel):
    """Card returned by the API."""

    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: UUID
    deck_id: UUID
    front: str
    back: str
    source: CardSource
    created_at: datetime
    updated_at: datetime


class CardBulkCreate(BaseModel):
    """Input model for creating cards in bulk."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "cards": [
                    {
                        "front": "Data quality is as important as model quality.",
                        "back": "A qualidade dos dados é tão importante quanto a qualidade do modelo.",
                        "source": "manual",
                    },
                    {
                        "front": "Small iterative improvements lead to robust systems.",
                        "back": "Pequenas melhorias iterativas levam a sistemas robustos.",
                        "source": "llm",
                    },
                ]
            }
        },
    )

    cards: list[CardBulkItemCreate] = Field(..., min_length=1)
