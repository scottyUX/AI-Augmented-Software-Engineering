"""RAG — policy-grounded answers.

Task: answer a customer question using ONLY the retrieved help-center text. If the
answer isn't in the docs, the model must say it doesn't know (don't hallucinate).

Fill in YOUR_SYSTEM_PROMPT and YOUR_RETRIEVER.
Run:  python rag.py
"""
import os
import re

from ollama import chat

MODEL = "llama3.1:8b"
DATA = os.path.join(os.path.dirname(__file__), "data", "help_center.txt")


def load_chunks() -> list[str]:
    with open(DATA, encoding="utf-8") as f:
        # one chunk per non-empty line
        return [line.strip() for line in f if line.strip()]


# TODO: return the subset of chunks relevant to `question` (simple keyword overlap is fine).
STOPWORDS = {
    "a", "an", "the", "is", "are", "do", "does", "you", "your", "i", "my", "me", "to",
    "of", "for", "in", "on", "and", "or", "what", "how", "can", "it", "have", "has",
    "long", "what's", "whats", "with", "we", "our", "be", "will", "if", "at", "by",
}
# Map question words to the words the help center actually uses.
SYNONYMS = {
    "ship": "shipping", "shipped": "shipping", "deliver": "delivery", "internationally": "international",
    "return": "returns", "returning": "returns", "refund": "returns", "pay": "billing",
    "payment": "billing", "charged": "billing", "card": "billing", "guarantee": "warranty",
    "contact": "support", "chat": "support", "hours": "support",
}


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9']+", text.lower())
    out = set()
    for w in words:
        w = w.strip("'")
        if not w or w in STOPWORDS:
            continue
        out.add(SYNONYMS.get(w, w))
        if w.endswith("s") and len(w) > 3:
            out.add(w[:-1])  # crude singular: "items" -> "item"
    return out


def YOUR_RETRIEVER(question: str, chunks: list[str], k: int = 3) -> list[str]:
    """Keyword-overlap retriever: score each chunk by shared tokens, keep the top k (score > 0)."""
    q = _tokens(question)
    scored = [(len(q & _tokens(chunk)), i, chunk) for i, chunk in enumerate(chunks)]
    scored = [s for s in scored if s[0] > 0]
    scored.sort(key=lambda s: (-s[0], s[1]))
    return [chunk for _, _, chunk in scored[:k]]


# TODO: Fill this in! Force the model to answer only from the provided context.
YOUR_SYSTEM_PROMPT = """You are a customer-support assistant for an online store.
Answer the question using ONLY the text under "Context". Do not use outside knowledge.
- If the context answers the question, reply in one or two sentences and reuse the
  context's own wording for key facts (numbers, places, time periods).
- If the context is empty or does not contain the answer, reply exactly:
  "I'm sorry, I don't know the answer to that based on our help center."
Never guess, never make up details, and never share personal information."""

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
