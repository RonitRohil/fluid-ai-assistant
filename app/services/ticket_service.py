import json

from app.config import DATA_DIR

_ticket_counter = [4]


class TicketService:
    def create(self, title: str, description: str, priority: str = "medium") -> dict:
        if priority not in ("low", "medium", "high"):
            priority = "medium"
        ticket_id = f"TKT-{_ticket_counter[0]:03d}"
        _ticket_counter[0] += 1
        return {
            "ticket_id": ticket_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "open",
            "message": f"Ticket {ticket_id} created successfully.",
        }

    def list_open(self, priority: str = None) -> dict:
        tickets = self._load()
        open_tickets = [t for t in tickets if t["status"] in ("open", "in_progress")]
        if priority:
            open_tickets = [
                t for t in open_tickets if t["priority"] == priority.lower()
            ]
        return {"open_tickets": open_tickets, "count": len(open_tickets)}

    def _load(self) -> list:
        with open(DATA_DIR / "tickets.json") as f:
            return json.load(f)


ticket_service = TicketService()
