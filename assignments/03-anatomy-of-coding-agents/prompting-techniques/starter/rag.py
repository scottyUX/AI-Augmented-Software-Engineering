"""RAG — policy-grounded answers."""
import os
import re

from ollama import chat

MODEL = "llama3.1:8b"
DATA = os.path.join(os.path.dirname(__file__), "data", "help_center.txt")
STOP_WORDS = {
    "a", "an", "and", "are", "do", "does", "for", "how", "i", "in", "is",
    "it", "me", "my", "of", "on", "the", "to", "what", "when", "where",
    "you", "your",
}


def load_chunks() -> list[str]:
    with open(DATA, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def _terms(text: str) -> set[str]:
    terms = set()
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        if word in STOP_WORDS:
            continue
        if word.endswith("ies") and len(word) > 4:
            word = word[:-3] + "y"
        elif word.endswith("s") and len(word) > 3:
            word = word[:-1]
        terms.add(word)
        if word.endswith("ly") and len(word) > 4:
            terms.add(word[:-2])
    return terms


def YOUR_RETRIEVER(question: str, chunks: list[str]) -> list[str]:
    question_terms = _terms(question)
    scored = [
        (len(question_terms & _terms(chunk)), index, chunk)
        for index, chunk in enumerate(chunks)
    ]
    relevant = [item for item in scored if item[0] > 0]
    relevant.sort(key=lambda item: (-item[0], item[1]))
    return [chunk for _, _, chunk in relevant]


YOUR_SYSTEM_PROMPT = """Answer the customer's question using only the supplied help
center context. Do not use outside knowledge or infer details that are not stated.
If the context does not contain the answer, politely say you don't know based on the
available information. Keep the answer concise."""

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
        ok = any(needle.lower() in got for needle in needles)
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {question!r} -> {got[:80]!r}")
    print(f"{passed}/{len(CASES)} correct")
    return passed == len(CASES)


if __name__ == "__main__":
    run()
