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
YOUR_SYSTEM_PROMPT = """You are an automated support ticket classification assistant for an online store.
Your task is to classify incoming customer messages into exactly one of the following five categories:
- billing: Questions or issues regarding charges, payment methods, receipts, or duplicate transactions.
- shipping: Questions about order tracking, delivery status, transit times, or missing packages.
- returns: Inquiries about product returns, exchanges, return policies, or refunds for returned items.
- technical: Issues with website errors, app bugs, checkout crashes, or login problems.
- other: Any general inquiries or feedback that do not fit into the four categories above.

Here are examples of how to classify messages:

Message: I was billed two times for my recent purchase.
Label: billing

Message: Can you tell me when my delivery will arrive? It is delayed.
Label: shipping

Message: How do I initiate a return for this jacket that doesn't fit?
Label: returns

Message: The website shows a 500 server error when I click place order.
Label: technical

Message: What are your store opening hours on holidays?
Label: other

Instructions:
- Classify the user's message into the single best category.
- Output ONLY the category name in lowercase (billing, shipping, returns, technical, or other).
- Do NOT output any punctuation, extra words, quotation marks, or explanation."""

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
