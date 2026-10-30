"""K-shot prompting — ticket classification."""
from ollama import chat

MODEL = "llama3.1:8b"
NUM_RUNS = 5

YOUR_SYSTEM_PROMPT = """You are a support-ticket classifier. Classify each customer
message using the examples below. Reply with exactly one lowercase label and nothing
else: billing, shipping, returns, technical, or other.

Examples:
Message: My card was charged twice for order 4412.
Label: billing

Message: Where is my package? It has been two weeks.
Label: shipping

Message: I want to send the shoes back for a refund.
Label: returns

Message: The app crashes every time I open my cart.
Label: technical

Message: Can I speak with a person about a question?
Label: other
"""

CASES = [
    ("My card was charged twice for order 4412.", "billing"),
    ("Where is my package? It's been two weeks.", "shipping"),
    ("I want to send the shoes back for a refund.", "returns"),
    ("The app crashes every time I open my cart.", "technical"),
]


def classify(system_prompt: str, message: str) -> str:
    resp = chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        options={"temperature": 0.0},
    )
    return resp.message.content.strip().lower()


def run() -> bool:
    passed = 0
    for message, expected in CASES:
        got = classify(YOUR_SYSTEM_PROMPT, message)
        ok = got == expected
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {message!r} -> got {got!r}, expected {expected!r}")
    print(f"{passed}/{len(CASES)} correct")
    return passed == len(CASES)


if __name__ == "__main__":
    run()
