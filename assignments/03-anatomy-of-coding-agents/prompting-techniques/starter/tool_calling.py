"""Tool calling — order lookup.

Task: the model must decide to call the `get_order_status` tool with the order id it
finds in the user's message, then use the returned status in a short reply.

Fill in YOUR_SYSTEM_PROMPT and the tool schema TODO.
Run:  python tool_calling.py
"""
from ollama import chat

MODEL = "llama3.1:8b"

FAKE_DB = {
    "4412": "shipped, arriving Friday",
    "9001": "processing",
}


def get_order_status(order_id: str) -> str:
    return FAKE_DB.get(order_id, "not found")


# TODO: describe the tool so the model knows when and how to call it.

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Look up the current status of a customer's order using its order ID. Call this function whenever a customer asks about an order's status, shipping progress, or delivery.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The exact order ID extracted from the customer's message, such as '4412'."
                    },
                },
                "required": ["order_id"],
            },
        },
    }
]


# TODO: Fill this in! Tell the model to look up the order before answering.

YOUR_SYSTEM_PROMPT = """You are a helpful customer support assistant for an online store.

When a customer asks about an order:
1. Identify the exact order ID in the customer's message.
2. Call the get_order_status tool using that order ID as a string.
3. Do not guess or invent an order status.
4. Use the tool's result to provide a short, accurate response when the result is available.

Always use get_order_status before answering an order status question.
"""


def run() -> bool:
    message = "Hi, can you check on order 4412 for me?"
    resp = chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": YOUR_SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        tools=TOOLS,
        options={"temperature": 0.0},
    )
    calls = resp.message.tool_calls or []
    if not calls:
        print("[FAIL] model did not call the tool")
        return False
    call = calls[0]
    order_id = str(call.function.arguments.get("order_id"))
    ok = order_id == "4412"
    print(f"[{'PASS' if ok else 'FAIL'}] tool called with order_id={order_id!r}")
    if ok:
        print("tool result:", get_order_status(order_id))
    return ok


if __name__ == "__main__":
    run()
