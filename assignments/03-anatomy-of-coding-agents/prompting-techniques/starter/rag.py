"""RAG — policy-grounded answers.

Task: answer a customer question using ONLY the retrieved help-center text. If the
answer isn't in the docs, the model must say it doesn't know (don't hallucinate).

Fill in YOUR_SYSTEM_PROMPT and YOUR_RETRIEVER.
Run:  python rag.py
"""
import os

from ollama import chat

MODEL = "llama3.1:8b"
DATA = os.path.join(os.path.dirname(__file__), "data", "help_center.txt")


def load_chunks() -> list[str]:
    with open(DATA, encoding="utf-8") as f:
        # one chunk per non-empty line
        return [line.strip() for line in f if line.strip()]


# TODO: return the subset of chunks relevant to `question` (simple keyword overlap is fine).

def YOUR_RETRIEVER(question: str, chunks: list[str]) -> list[str]:
    question_lower = question.lower()

    keywords = {
        "returns": ["return", "refund", "exchange"],
        "shipping": ["ship", "shipping", "delivery", "international"],
        "billing": ["payment", "pay", "charged", "billing", "visa", "mastercard", "paypal", "card"],
        "warranty": ["warranty", "guarantee", "defect"],
        "support": ["support", "chat", "contact", "hours"],
    }

    relevant_chunks = []

    for chunk in chunks:
        category = chunk.split(":")[0].lower()
        category_keywords = keywords.get(category, [])

        if any(word in question_lower for word in category_keywords):
            relevant_chunks.append(chunk)

    return relevant_chunks


# TODO: Fill this in! Force the model to answer only from the provided context.

YOUR_SYSTEM_PROMPT = """You are a customer support assistant for an online store.

Answer customer questions using ONLY the information provided in the Context section.

Rules:
1. Read the provided context carefully.
2. Answer only with facts explicitly supported by the context.
3. Do not use outside knowledge or make assumptions.
4. If the context is empty or does not contain the answer, politely say:
   "I don't know based on the available help-center information."
5. Keep your response short, clear, and helpful.
6. Never invent policies, shipping details, personal information, or other facts.
"""


CASES = [
    ("How long do I have to return an item?", ["30 days"]),
    ("Do you ship internationally?", ["international"]),
    ("What's your CEO's home address?", ["don't know", "do not know", "not sure", "cannot"]),
]


def answer(question: str) -> str:
    context = "\n".join(YOUR_RETRIEVER(question, load_chunks()))
    resp = chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": YOUR_SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
        options={"temperature": 0.0},
    )
    return resp.message.content.strip().lower()


def run() -> bool:
    passed = 0
    for question, needles in CASES:
        got = answer(question)
        ok = any(n.lower() in got for n in needles)
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {question!r} -> {got[:80]!r}")
    print(f"{passed}/{len(CASES)} correct")
    return passed == len(CASES)


if __name__ == "__main__":
    run()
