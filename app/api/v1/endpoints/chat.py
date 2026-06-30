from fastapi import APIRouter

from app.core.agent import run_agent
from app.schemas.chat import AskRequest, AskResponse
from app.services.session_service import session_service

router = APIRouter()


@router.post(
    "/ask", response_model=AskResponse, summary="Send a message to the AI assistant"
)
async def ask(request: AskRequest):
    question = request.question.strip()
    session_id = request.session_id or "default"
    history = session_service.get_history(session_id)

    try:
        answer, action_taken = run_agent(question, history)
    except Exception as e:
        print(f"Agent error: {e}")
        return AskResponse(
            answer="Sorry, I ran into an issue processing your request. Please try again.",
            action_taken=None,
            session_id=session_id,
        )

    session_service.append(session_id, question, answer)
    return AskResponse(answer=answer, action_taken=action_taken, session_id=session_id)
