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
YOUR_SYSTEM_PROMPT = """You are a refund-eligibility assistant for an online store.
Decide whether the customer's order qualifies for a refund under the refund policy given at the end of this message.

Think step by step. Check each rule and write one short line per rule:
1. Days since purchase: is it 30 days or fewer?
2. Condition: is the item unused / in original condition? If not mentioned, assume unused.
3. Final sale: is it a final-sale item? If not mentioned, assume it is NOT final sale.
The refund is allowed only if ALL rules pass. If ANY rule fails, it is not allowed.

OUTPUT FORMAT (mandatory, even after reading the policy):
Your answer MUST end with a final line that is exactly "DECISION: YES" or "DECISION: NO".
Never end your answer without this line, and write nothing after it.

Example answer:
1. Days since purchase: 12 days, within 30 days. PASS
2. Condition: unused. PASS
3. Final sale: not mentioned, so not final sale. PASS
All rules pass, so the refund is allowed.
DECISION: YES"""

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
