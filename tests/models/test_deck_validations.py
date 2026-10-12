from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models.deck import DeckCreate, DeckUpdate


@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_deck_create_rejects_empty_or_blank_name(invalid_name: str) -> None:
    with pytest.raises(ValidationError):
        DeckCreate(name=invalid_name, description="Descricao valida")


def test_deck_create_trims_valid_name() -> None:
    deck = DeckCreate(name="  Deck de Ingles  ", description="Descricao")
    assert deck.name == "Deck de Ingles"


def test_deck_create_rejects_name_above_max_length() -> None:
    with pytest.raises(ValidationError):
        DeckCreate(name="a" * 121, description="Descricao valida")


def test_deck_create_accepts_name_at_max_length() -> None:
    deck = DeckCreate(name="a" * 120, description="Descricao valida")
    assert len(deck.name) == 120


def test_deck_create_converts_blank_description_to_none() -> None:
    deck = DeckCreate(name="Deck Valido", description="   ")
    assert deck.description is None


def test_deck_create_rejects_description_above_max_length() -> None:
    with pytest.raises(ValidationError):
        DeckCreate(name="Deck Valido", description="d" * 501)


def test_deck_create_accepts_description_at_max_length() -> None:
    deck = DeckCreate(name="Deck Valido", description="d" * 500)
    assert deck.description is not None
    assert len(deck.description) == 500


@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_deck_update_rejects_empty_or_blank_name(invalid_name: str) -> None:
    with pytest.raises(ValidationError):
        DeckUpdate(name=invalid_name)


def test_deck_update_allows_empty_payload() -> None:
    payload = DeckUpdate()
    assert payload.name is None
    assert payload.description is None


def test_deck_update_trims_valid_description() -> None:
    payload = DeckUpdate(description="  Nova descricao  ")
    assert payload.description == "Nova descricao"


def test_deck_update_rejects_blank_description() -> None:
    with pytest.raises(ValidationError):
        DeckUpdate(description="   ")


def test_deck_update_rejects_name_above_max_length() -> None:
    with pytest.raises(ValidationError):
        DeckUpdate(name="a" * 121)


def test_deck_update_accepts_name_at_max_length() -> None:
    payload = DeckUpdate(name="a" * 120)
    assert len(payload.name or "") == 120
