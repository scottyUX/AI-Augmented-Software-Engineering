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


# Return the subset of chunks relevant to `question` using normalized keyword overlap.
def YOUR_RETRIEVER(question: str, chunks: list[str]) -> list[str]:
    stop_words = {
        "a", "an", "do", "does", "for", "how", "i", "is", "it", "my",
        "of", "the", "to", "what", "when", "where", "you", "your",
    }

    def words(text: str) -> list[str]:
        return [
            cleaned
            for word in text.lower().split()
            if (cleaned := "".join(char for char in word if char.isalnum()))
            and cleaned not in stop_words
        ]

    def related(left: str, right: str) -> bool:
        return left == right or (
            len(left) >= 4
            and len(right) >= 4
            and (left.startswith(right) or right.startswith(left))
        )

    question_words = words(question)
    return [
        chunk
        for chunk in chunks
        if any(
            related(question_word, chunk_word)
            for question_word in question_words
            for chunk_word in words(chunk)
        )
    ]


# Force the model to answer only from the provided context.
YOUR_SYSTEM_PROMPT = """You are a customer support bot.

Use the provided context to answer the customer's question. Find the necessary information in the context and give an appropriate answer to the customer.

Use only the information in the provided context when answering.

If the answer to the question is not in the context, reply exactly: I do not know based on the provided information.

Do not use your own knowledge outside the context.

Do not invent information or make guesses or assumptions.

Keep your answer short and clear.
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
