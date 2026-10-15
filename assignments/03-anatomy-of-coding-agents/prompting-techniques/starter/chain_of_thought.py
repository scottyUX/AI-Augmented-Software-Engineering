"""Chain-of-thought — refund eligibility.

Task: given the refund policy and an order, decide YES or NO. Use chain-of-thought
so the model reasons step by step, but make the FINAL line exactly `DECISION: YES`
or `DECISION: NO` so it can be graded.

Only edit YOUR_SYSTEM_PROMPT.
Run:  python chain_of_thought.py
"""
from ollama import chat

MODEL = "llama3.1:8b"

POLICY = """Refund policy:
- Refunds allowed within 30 days of purchase.
- Item must be unused / in original condition.
- Final-sale items are never refundable.
"""

# TODO: Fill this in! Encourage step-by-step reasoning, ending with DECISION: YES/NO.
YOUR_SYSTEM_PROMPT = """You are a customer support agent evaluating refund eligibility.
Using the refund policy provided, evaluate the customer's request step-by-step:
1. Purchase Date Check: Was the purchase made within 30 days?
2. Item Condition Check: Is the item unused and in original condition?
3. Sale Type Check: Is the item non-final-sale (i.e. not marked as final sale)?

All three conditions must be satisfied for a refund to be approved. If any condition is violated or not met, the refund must be denied.

Provide a concise, step-by-step reasoning for each condition.
Then, conclude your response with the decision on the very last line.
The very last line of your response MUST be exactly either:
DECISION: YES
or
DECISION: NO

Do not append any text, punctuation, or comments after this final line."""

CASES = [
    ("Bought 10 days ago, unused, not final sale.", "YES"),
    ("Bought 45 days ago, unused.", "NO"),
    ("Bought 5 days ago but it was a final-sale item.", "NO"),
]


def decide(system_prompt: str, order: str) -> str:
    resp = chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt + "\n" + POLICY},
            {"role": "user", "content": order},
        ],
        options={"temperature": 0.0},
    )
    text = resp.message.content.strip()
    last = text.splitlines()[-1].upper() if text else ""
    return "YES" if "DECISION: YES" in last else "NO" if "DECISION: NO" in last else "?"


def run() -> bool:
    passed = 0
    for order, expected in CASES:
        got = decide(YOUR_SYSTEM_PROMPT, order)
        ok = got == expected
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {order!r} -> {got}, expected {expected}")
    print(f"{passed}/{len(CASES)} correct")
    return passed == len(CASES)


if __name__ == "__main__":
    run()
