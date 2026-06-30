from fastapi import APIRouter

from app.services.session_service import session_service

router = APIRouter()


@router.get("/{session_id}", summary="Retrieve conversation history for a session")
def get_history(session_id: str):
    return {
        "session_id": session_id,
        "history": session_service.get_history(session_id),
    }


@router.delete("/{session_id}", summary="Clear conversation history for a session")
def clear_history(session_id: str):
    session_service.clear(session_id)
    return {"message": f"History cleared for session '{session_id}'"}
