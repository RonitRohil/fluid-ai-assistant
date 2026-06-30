TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_employee_info",
            "description": "Look up employee information by name, employee ID, department, or role.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Name, ID, department, or role to search for",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_ticket",
            "description": "Create a new support or engineering ticket in the system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Short title for the ticket",
                    },
                    "description": {
                        "type": "string",
                        "description": "Detailed description of the issue",
                    },
                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                },
                "required": ["title", "description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_open_tickets",
            "description": "List all currently open support tickets. Optionally filter by priority.",
            "parameters": {
                "type": "object",
                "properties": {
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Optional priority filter",
                    }
                },
            },
        },
    },
]
