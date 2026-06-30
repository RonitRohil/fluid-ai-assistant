from app.services.employee_service import employee_service
from app.services.ticket_service import ticket_service


def _get_employee_info(query: str) -> dict:
    return employee_service.search(query)


def _create_ticket(title: str, description: str, priority: str = "medium") -> dict:
    return ticket_service.create(title, description, priority)


def _list_open_tickets(priority: str = None) -> dict:
    return ticket_service.list_open(priority)


TOOL_MAP: dict[str, callable] = {
    "get_employee_info": _get_employee_info,
    "create_ticket": _create_ticket,
    "list_open_tickets": _list_open_tickets,
}
