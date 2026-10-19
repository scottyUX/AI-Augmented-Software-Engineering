"""K-shot prompting — ticket classification.

Task: classify a customer message into one of: billing, shipping, returns,
technical, other. Use in-context EXAMPLES (k-shot) so the model outputs exactly the
label, lowercase, with no extra text.

Only edit YOUR_SYSTEM_PROMPT.
Run:  python k_shot_prompting.py
"""
from ollama import chat

MODEL = "llama3.1:8b"
NUM_RUNS = 5

# TODO: Fill this in! Include a few labeled examples (k-shot) in the system prompt.
YOUR_SYSTEM_PROMPT = """You are a support-ticket classifier for an online store.
Classify the customer's message into exactly one label:
billing, shipping, returns, technical, other

Label meanings:
- billing: payments, charges, invoices, refunds of money already charged, coupons
- shipping: delivery status, tracking, late or lost packages, shipping cost or address
- returns: sending an item back, exchanges, return labels, return eligibility
- technical: the website or app is broken, errors, crashes, login or password problems
- other: anything else

Reply with ONLY the label, in lowercase, with no punctuation and no explanation.

Examples:
Message: I was billed for a subscription I cancelled last month.
Label: billing

Message: The tracking number you sent doesn't work and my parcel hasn't arrived.
Label: shipping

Message: These headphones don't fit, how do I return them?
Label: returns

Message: I get an error 500 when I click checkout.
Label: technical

Message: Do you have a store in Berlin?
Label: other

Message: Why is there an extra $4 fee on my receipt?
Label: billing

Message: Can I exchange this jacket for a bigger size?
Label: returns

Message: The page keeps logging me out after one minute.
Label: technical"""

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
