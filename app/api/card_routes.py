"""Card routes for the flashcards API."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, status

from app.models.card import CardBulkCreate, CardCreate, CardOut, CardUpdate
from app.services.card_service import CardDeckNotFoundError, CardNotFoundError, CardService

router = APIRouter(prefix="/cards", tags=["cards"])
deck_cards_router = APIRouter(prefix="/decks", tags=["cards"])
service = CardService()


@router.get("", response_model=list[CardOut])
def list_cards() -> list[CardOut]:
    """List all cards."""
    return service.list_cards()


@router.post(
    "",
    response_model=CardOut,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Erro de regra de negócio.",
            "content": {
                "application/json": {
                    "example": {"detail": "deck_id is required to create a card"}
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Deck não encontrado.",
            "content": {
                "application/json": {
                    "example": {"detail": "Deck '3fa85f64-5717-4562-b3fc-2c963f66afa6' not found."}
                }
            },
        },
    },
)
def create_card(payload: CardCreate) -> CardOut:
    """Create a new card."""
    try:
        return service.create_card(payload)
    except CardDeckNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get(
    "/{card_id}",
    response_model=CardOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Card não encontrado.",
            "content": {
                "application/json": {
                    "example": {"detail": "Card '3fa85f64-5717-4562-b3fc-2c963f66afa6' not found."}
                }
            },
        }
    },
)
def get_card(card_id: UUID) -> CardOut:
    """Return a card by identifier."""
    try:
        return service.get_card_by_id(card_id)
    except CardNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put(
    "/{card_id}",
    response_model=CardOut,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Erro de regra de negócio.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "at least one field must be provided for card update"
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Card não encontrado.",
            "content": {
                "application/json": {
                    "example": {"detail": "Card '3fa85f64-5717-4562-b3fc-2c963f66afa6' not found."}
                }
            },
        },
    },
)
def update_card(card_id: UUID, payload: CardUpdate) -> CardOut:
    """Update an existing card."""
    try:
        return service.update_card(card_id, payload)
    except CardNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete(
    "/{card_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Card não encontrado.",
            "content": {
                "application/json": {
                    "example": {"detail": "Card '3fa85f64-5717-4562-b3fc-2c963f66afa6' not found."}
                }
            },
        }
    },
)
def delete_card(card_id: UUID) -> Response:
    """Delete a card by identifier."""
    try:
        service.delete_card(card_id)
    except CardNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@deck_cards_router.post(
    "/{deck_id}/cards/bulk",
    response_model=list[CardOut],
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Deck não encontrado.",
            "content": {
                "application/json": {
                    "example": {"detail": "Deck '3fa85f64-5717-4562-b3fc-2c963f66afa6' not found."}
                }
            },
        },
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "description": "Erro de validação de payload.",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "cards", 0, "source"],
                                "msg": "Input should be 'manual' or 'llm'",
                                "type": "literal_error",
                            }
                        ]
                    }
                }
            },
        },
    },
)
def create_cards_bulk(deck_id: UUID, payload: CardBulkCreate) -> list[CardOut]:
    """Create cards in bulk for a given deck."""
    try:
        return service.create_cards_bulk(deck_id=deck_id, payload=payload)
    except CardDeckNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
