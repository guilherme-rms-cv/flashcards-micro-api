"""Deck routes for the flashcards API."""

from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, status

from app.models.deck import DeckCreate, DeckOut, DeckUpdate
from app.services.deck_service import DeckNotFoundError, DeckService

router = APIRouter(prefix="/decks", tags=["decks"])
service = DeckService()


@router.get("", response_model=list[DeckOut])
def list_decks() -> list[DeckOut]:
    """List all decks."""
    return service.list_decks()


@router.post("", response_model=DeckOut, status_code=status.HTTP_201_CREATED)
def create_deck(payload: DeckCreate) -> DeckOut:
    """Create a new deck."""
    return service.create_deck(payload)


@router.get(
    "/{deck_id}",
    response_model=DeckOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Deck não encontrado.",
            "content": {
                "application/json": {
                    "example": {"detail": "Deck '3fa85f64-5717-4562-b3fc-2c963f66afa6' not found."}
                }
            },
        }
    },
)
def get_deck(deck_id: UUID) -> DeckOut:
    """Return a deck by identifier."""
    try:
        return service.get_deck_by_id(deck_id)
    except DeckNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put(
    "/{deck_id}",
    response_model=DeckOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Deck não encontrado.",
            "content": {
                "application/json": {
                    "example": {"detail": "Deck '3fa85f64-5717-4562-b3fc-2c963f66afa6' not found."}
                }
            },
        }
    },
)
def update_deck(deck_id: UUID, payload: DeckUpdate) -> DeckOut:
    """Update an existing deck."""
    try:
        return service.update_deck(deck_id, payload)
    except DeckNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete(
    "/{deck_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Deck não encontrado.",
            "content": {
                "application/json": {
                    "example": {"detail": "Deck '3fa85f64-5717-4562-b3fc-2c963f66afa6' not found."}
                }
            },
        }
    },
)
def delete_deck(deck_id: UUID) -> Response:
    """Delete a deck by identifier."""
    try:
        service.delete_deck(deck_id)
    except DeckNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return Response(status_code=status.HTTP_204_NO_CONTENT)
