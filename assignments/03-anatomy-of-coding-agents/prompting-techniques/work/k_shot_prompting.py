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
YOUR_SYSTEM_PROMPT = """You are a support-ticket router for an online store.
Classify the customer's message into exactly ONE label:
billing, shipping, returns, technical, other

Label meanings:
- billing: charges, payments, invoices, refunds that have not been issued, promo codes
- shipping: where an order is, delivery times, tracking, wrong address
- returns: sending an item back, exchanging it, starting a return
- technical: the website or app is broken, crashes, errors, login problems
- other: anything else

Reply with the label only: one lowercase word, no punctuation, no explanation.

Examples:
Message: I was billed $40 but my order total was $25.
Label: billing
Message: My tracking number hasn't updated in five days.
Label: shipping
Message: The jacket is too small, how do I return it?
Label: returns
Message: I get a 500 error when I try to log in.
Label: technical
Message: Do you have a physical store in Amman?
Label: other
Message: Can I pay with PayPal instead of my card?
Label: billing
Message: The package arrived at the wrong address.
Label: shipping
Message: I'd like to exchange these headphones for a different color.
Label: returns
Message: The checkout button does nothing when I tap it.
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
