# Week 3 — Prompting Techniques: The Support-Desk Assistant

## Technique 1: K-Shot Prompting (`k_shot_prompting.py`)
**Final Prompt:**
```text
Classify the customer message into one of: billing, shipping, returns, technical, other.
Output exactly the label, lowercase, with no extra text or punctuation.

Message: "I need to update my payment method."
billing

Message: "My order is delayed, can you check the status?"
shipping

Message: "How do I print a return label?"
returns

Message: "The website won't let me reset my password."
technical

Message: "Do you have physical stores?"
other
```
**Sample Input / Output:**
* **Input:** `'My card was charged twice for order 4412.'`
* **Output:** `'billing'`

**What I Learned:** 
In-context examples (k-shot) force the LLM to follow precise output formatting without conversational clutter or unnecessary text.

---

## Technique 2: Chain-of-Thought (`chain_of_thought.py`)
**Final Prompt:**
```text
You are a refund evaluation assistant. Analyze the user's order details against the provided refund policy. 

Think step-by-step and write out your reasoning:
1. Is the purchase within the 30-day window?
2. Is the item unused and in original condition?
3. Is it a final-sale item?

After writing out your reasoning, your very last line MUST be exactly:
DECISION: YES
or
DECISION: NO
```
**Sample Input / Output:**
* **Input:** `'Bought 45 days ago, unused.'`
* **Output:** `'NO'`

**What I Learned:** 
Forcing the LLM to explicitly write out its reasoning against a checklist before stating the final answer prevents logical leaps and improves accuracy on multi-constraint problems.

---

## Technique 3: Tool Calling (`tool_calling.py`)
**Final Prompt & Tool Definition:**
* **System Prompt:**
```text
You are a helpful customer support assistant. When a customer asks about the status of an order, you must call the `get_order_status` tool using the order ID provided in the message to check its status before answering.
```
* **Tool Description:** `"Look up the current fulfillment or shipping status of a customer order using its order ID."`

**Sample Input / Output:**
* **Input:** `"Hi, can you check on order 4412 for me?"`
* **Output:** Tool call `get_order_status(order_id='4412')` returning `"shipped, arriving Friday"`

**What I Learned:** 
Tool calling allows the LLM to access real-time or private dynamic data (like databases) by emitting structured function calls instead of trying to hallucinate external facts.

---

## Technique 4: RAG (`rag.py`)
**Final Prompt:**
```text
You are a helpful customer support assistant. Answer the user's question using ONLY the information provided in the Context section below.

Rules:
1. Do not use outside knowledge or assumptions.
2. If the answer is not contained in the provided Context, explicitly state: "I don't know."
3. Keep your response concise and direct.
```
**Sample Input / Output:**
* **Input:** `"What's your CEO's home address?"`
* **Output:** `"i don't know."`

**What I Learned:** 
Providing a specific context and strictly instructing the LLM to only use that data (and to refuse answering if the data is missing) effectively eliminates hallucinations.

---

## Conclusion: Why LLMs Need Scaffolding
Across all four techniques, I learned that while LLMs are incredibly powerful at understanding natural language, they struggle with strict formatting, complex multi-step logic, accessing real-time data, and staying grounded in facts without external scaffolding. K-shot prompting forces structural compliance, chain-of-thought enforces logical reasoning, tool calling connects the model to dynamic real-world systems, and RAG provides a reliable, hallucination-free knowledge base. By wrapping the raw model in these structured constraints, we can transform it from an unpredictable text generator into a reliable, structured software agent.