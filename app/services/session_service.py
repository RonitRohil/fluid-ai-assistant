from app.config import MAX_HISTORY


class SessionService:
    _store: dict[str, list] = {}

    def get_history(self, session_id: str) -> list:
        return list(self._store.get(session_id, []))

    def append(self, session_id: str, question: str, answer: str) -> None:
        history = self._store.get(session_id, [])
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        self._store[session_id] = history[-MAX_HISTORY:]

    def clear(self, session_id: str) -> None:
        self._store.pop(session_id, None)


session_service = SessionService()
