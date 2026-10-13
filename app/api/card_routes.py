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


@router.post("", response_model=CardOut, status_code=status.HTTP_201_CREATED)
def create_card(payload: CardCreate) -> CardOut:
    """Create a new card."""
    try:
        return service.create_card(payload)
    except CardDeckNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{card_id}", response_model=CardOut)
def get_card(card_id: UUID) -> CardOut:
    """Return a card by identifier."""
    try:
        return service.get_card_by_id(card_id)
    except CardNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{card_id}", response_model=CardOut)
def update_card(card_id: UUID, payload: CardUpdate) -> CardOut:
    """Update an existing card."""
    try:
        return service.update_card(card_id, payload)
    except CardNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
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
)
def create_cards_bulk(deck_id: UUID, payload: CardBulkCreate) -> list[CardOut]:
    """Create cards in bulk for a given deck."""
    try:
        return service.create_cards_bulk(deck_id=deck_id, payload=payload)
    except CardDeckNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
