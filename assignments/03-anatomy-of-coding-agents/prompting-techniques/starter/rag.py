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
    stopwords = {
        "a", "an", "the", "i", "you", "your", "my", "is", "are", "do", "does",
        "to", "of", "in", "on", "for", "how", "what", "where", "have", "can",
        "it", "item", "items", "this", "that"
    }
    stem_map = {
        "internationally": "international",
        "returns": "return",
        "shipping": "ship",
        "ships": "ship",
        "refunds": "refund",
    }
    words = [w.strip(".,?!:;\"'()[]{}") for w in question.lower().split()]
    q_tokens = {stem_map.get(w, w) for w in words if w and w not in stopwords}

    scored_chunks = []
    for chunk in chunks:
        c_words = [w.strip(".,?!:;\"'()[]{}") for w in chunk.lower().split()]
        c_tokens = {stem_map.get(w, w) for w in c_words if w}
        overlap = len(q_tokens & c_tokens)
        if overlap > 0:
            scored_chunks.append((overlap, chunk))

    # Sort descending by overlap score
    scored_chunks.sort(key=lambda item: -item[0])
    return [chunk for _, chunk in scored_chunks]


# TODO: Fill this in! Force the model to answer only from the provided context.
YOUR_SYSTEM_PROMPT = """You are a helpful customer support assistant for an online store.
Answer the customer's question using ONLY the factual information provided in the Context below.
Rules:
1. Answer strictly based on the Context. Do not bring in outside knowledge or make assumptions.
2. If the Context is empty or does not contain the information needed to answer the question, politely say: "I do not know based on the available information."
3. Keep the response concise, polite, and directly grounded in the provided text."""

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
