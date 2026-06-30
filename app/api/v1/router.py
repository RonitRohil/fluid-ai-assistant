from fastapi import APIRouter

from app.api.v1.endpoints import chat, session

router = APIRouter()

router.include_router(chat.router, tags=["Chat"])
router.include_router(session.router, prefix="/history", tags=["Session"])
