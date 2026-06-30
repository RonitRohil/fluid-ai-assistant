import json

from openai import OpenAI

from app.config import GROQ_API_KEY, GROQ_BASE_URL, MODEL_NAME, MAX_TOOL_ITERATIONS
from app.tools.definitions import TOOLS
from app.tools.registry import TOOL_MAP

client = OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

SYSTEM_PROMPT = """You are an AI enterprise assistant for ACME Corp. You help employees with:
- Finding employee information
- Creating support tickets
- Checking open tickets and their status

Use the available tools when needed. If a request is unclear, ask for clarification.
If a request is outside your scope (e.g., financial advice, personal tasks), politely decline.
Always be concise and professional."""


def run_agent(question: str, history: list) -> tuple[str, str | None]:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": question})

    action_taken = None

    for _ in range(MAX_TOOL_ITERATIONS):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2,
        )

        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content, action_taken

        messages.append(msg)

        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)

            if fn_name not in TOOL_MAP:
                result = {"error": f"Unknown tool: {fn_name}"}
            else:
                result = TOOL_MAP[fn_name](**fn_args)
                action_taken = f"{fn_name}({fn_args})"

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result),
                }
            )

    return (
        "I wasn't able to complete that request. Please try rephrasing.",
        action_taken,
    )
