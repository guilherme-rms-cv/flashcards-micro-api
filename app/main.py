from datetime import datetime, timezone
from typing import Literal, TypedDict

from fastapi import FastAPI

from app.api.deck_routes import router as deck_router


class HealthResponse(TypedDict):
    status: Literal["ok"]
    timestamp: str


app = FastAPI(title="Flashcards Micro-API")

app.include_router(deck_router)


@app.get("/health")
def health_check() -> HealthResponse:
    current_timestamp = datetime.now(timezone.utc).isoformat()
    return {
        "status": "ok",
        "timestamp": current_timestamp,
    }
