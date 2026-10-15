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

# The system prompt defines the labels, provides k-shot examples, and constrains output.
YOUR_SYSTEM_PROMPT = """You are a customer support message classifier.

Your task is to classify messages from customers into only one of the categories below.

The allowed categories are:

billing: Problems related to payments, invoices, or charges.

shipping: Problems related to shipping, delivery, or when a product will arrive.

returns: Requests related to returning or exchanging a product.

technical: Technical problems with the application or website.

other: Messages that do not belong to any of the categories above.

Example messages:

Customer: "I bought the product in 3 installments, but it appears as a single payment on my invoice."
Answer: billing

Customer: "When will my product arrive? I have been waiting for 2 weeks."
Answer: shipping

Customer: "I want to return the shoes. What should I do?"
Answer: returns

Customer: "I want to make a purchase in the app, but I cannot complete it."
Answer: technical

Customer: "Is your store open on weekends?"
Answer: other

Output rules:

- The output must be only one word.
- Use only one of these 5 words: billing, shipping, returns, technical, other.
- Write the word in lowercase.
- Do not add an explanation, sentence, or punctuation mark.
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
