from datetime import datetime, timezone
from typing import Literal, TypedDict

from fastapi import FastAPI

from app.api.card_routes import deck_cards_router, router as card_router
from app.api.deck_routes import router as deck_router


class HealthResponse(TypedDict):
    status: Literal["ok"]
    timestamp: str


app = FastAPI(title="Flashcards Micro-API")

app.include_router(deck_router)
app.include_router(card_router)
app.include_router(deck_cards_router)


@app.get("/health")
def health_check() -> HealthResponse:
    current_timestamp = datetime.now(timezone.utc).isoformat()
    return {
        "status": "ok",
        "timestamp": current_timestamp,
    }
