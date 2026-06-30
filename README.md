# FluidAI Enterprise Assistant

An AI-powered enterprise assistant built with FastAPI and an LLM tool-calling (agentic) loop. Employees can ask natural-language questions to look up colleagues, create support tickets, and check ticket status — the agent decides which tools to invoke automatically.

---

## Architecture

```
User Request (POST /api/v1/ask)
        │
        ▼
   FastAPI  (app/main.py)
   ┌────────────────────────┐
   │  Pydantic validation   │
   │  API versioning (v1)   │
   └──────────┬─────────────┘
              │
              ▼
   Session Service          ← retrieves conversation history
              │
              ▼
   Agent  (app/core/agent.py)
   ┌────────────────────────┐
   │  System prompt         │
   │  + History             │
   │  + User question       │
   │          │             │
   │   Groq API (LLM)       │
   │          │             │
   │  Tool call? ──Yes──────┼──► Tool Registry
   │          │             │     ├── EmployeeService
   │         No             │     └── TicketService
   │          │             │              │
   │   Final answer ◄───────┼──────────────┘
   └────────────────────────┘
              │
              ▼
   Session Service          ← persists updated history
              │
              ▼
   AskResponse (JSON)
```

### Layer responsibilities

| Layer | Path | Responsibility |
|---|---|---|
| API | `app/api/v1/endpoints/` | HTTP request/response, versioning |
| Core | `app/core/agent.py` | LLM reasoning loop, tool orchestration |
| Schemas | `app/schemas/` | Pydantic request/response models |
| Services | `app/services/` | Business logic (employees, tickets, sessions) |
| Tools | `app/tools/` | OpenAI tool schemas + dispatcher registry |
| Config | `app/config.py` | All env vars and path constants |

---

## Project Structure

```
fluid-ai-assistant/
├── main.py                              # Entry point
├── .env                                 # Secret keys (never commit)
├── .env.example                         # Template for .env
├── requirements.txt
├── mock_data/
│   ├── employees.json
│   └── tickets.json
└── app/
    ├── main.py                          # FastAPI app factory + lifespan
    ├── config.py                        # Centralised env vars & constants
    ├── api/
    │   └── v1/
    │       ├── router.py                # Aggregates all v1 routes
    │       └── endpoints/
    │           ├── chat.py              # POST /api/v1/ask
    │           └── session.py           # GET/DELETE /api/v1/history/{session_id}
    ├── core/
    │   └── agent.py                     # Tool-calling loop (LLM logic)
    ├── schemas/
    │   └── chat.py                      # AskRequest / AskResponse
    ├── services/
    │   ├── employee_service.py          # Employee search logic
    │   ├── ticket_service.py            # Ticket create/list logic
    │   └── session_service.py           # In-memory conversation history
    └── tools/
        ├── definitions.py               # OpenAI function-calling JSON schemas
        └── registry.py                  # Maps tool names → service calls
```

---

## Setup

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd fluid-ai-assistant

python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your Groq API key:

```env
GROQ_API_KEY=your-groq-api-key-here
MODEL_NAME=llama-3.3-70b-versatile
MAX_HISTORY=10
MAX_TOOL_ITERATIONS=3
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

### 4. Start the server

```bash
uvicorn app.main:app --reload --port 8000
```

Or via the root entry point:

```bash
python main.py
```

---

## API Reference

Interactive docs are available at `http://localhost:8000/docs` once the server is running.

### `GET /health`
Returns server status.

```bash
curl http://localhost:8000/health
```

```json
{ "status": "ok", "version": "1.0.0" }
```

---

### `POST /api/v1/ask`
Send a natural-language question to the assistant.

**Request body:**

| Field | Type | Required | Description |
|---|---|---|---|
| `question` | string | Yes | The user's question (1–1000 chars) |
| `session_id` | string | No | Session identifier for conversation history (default: `"default"`) |

**Example — employee lookup:**

```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Who is the HR lead and what is their email?", "session_id": "demo"}'
```

```json
{
  "answer": "The HR Lead is Anita Kapoor. You can reach her at anita@acme.com.",
  "action_taken": "get_employee_info({'query': 'HR lead'})",
  "session_id": "demo"
}
```

**Example — create a ticket:**

```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Create a high-priority ticket: Safari login page is broken", "session_id": "demo"}'
```

```json
{
  "answer": "Done! I've created ticket TKT-004 titled 'Safari login page is broken' with high priority.",
  "action_taken": "create_ticket({'title': 'Safari login page is broken', 'description': '...', 'priority': 'high'})",
  "session_id": "demo"
}
```

**Example — list open tickets:**

```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me all open high-priority tickets", "session_id": "demo"}'
```

**Example — out-of-scope guardrail:**

```bash
curl -X POST http://localhost:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What stocks should I buy today?", "session_id": "demo"}'
```

```json
{
  "answer": "That's outside my scope. I can help you find employee information, create support tickets, or check ticket status.",
  "action_taken": null,
  "session_id": "demo"
}
```

---

### `GET /api/v1/history/{session_id}`
Returns conversation history for a session.

```bash
curl http://localhost:8000/api/v1/history/demo
```

---

### `DELETE /api/v1/history/{session_id}`
Clears conversation history for a session.

```bash
curl -X DELETE http://localhost:8000/api/v1/history/demo
```

---

## Available Tools

The agent automatically selects and calls these tools based on the user's question:

| Tool | Description |
|---|---|
| `get_employee_info` | Search employees by name, ID, department, or role |
| `create_ticket` | Create a new support ticket with title, description, and priority |
| `list_open_tickets` | List all open/in-progress tickets, with optional priority filter |

---

## Design Decisions

**Groq + LLaMA 3.3 70B over OpenAI GPT-4o**
Groq's inference is significantly faster (low latency is critical for a chat interface) and the free tier is generous enough for development and demo purposes. The OpenAI-compatible client means swapping providers requires changing two lines in `config.py`.

**Tool-calling loop capped at 3 iterations**
Prevents runaway chains while still allowing multi-step reasoning (e.g. look up employee → confirm → create ticket). Configurable via `MAX_TOOL_ITERATIONS` in `.env`.

**In-memory session store**
Simple and zero-dependency — appropriate for a demo. In production, replace `SessionService._store` with a Redis client and add TTL-based expiry per session.

**API versioning (`/api/v1/`)**
Adding a `v2` endpoint is a new folder under `app/api/` with no changes to existing routes. Zero breaking changes for existing clients.

**Services own business logic, tools own the LLM contract**
`EmployeeService.search()` and `TicketService.create()` can be unit-tested without touching the LLM. The tool registry (`app/tools/registry.py`) is the only place that wires them together.

---

## Tradeoffs

| Decision | Current choice | Production alternative |
|---|---|---|
| Session storage | In-memory dict | Redis with TTL |
| Data persistence | JSON files | PostgreSQL / Elasticsearch |
| LLM routing | Single model for all queries | Route simple lookups to a smaller/faster model |
| Auth | None | API key or OAuth2 via FastAPI middleware |
| Observability | `print()` statements | Structured logging + Sentry / Datadog |
