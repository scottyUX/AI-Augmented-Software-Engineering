# Week 3 — Prompting Techniques: The Support-Desk Assistant

## 1. Introduction

This assignment explores four prompting techniques using the locally hosted `llama3.1:8b` model through Ollama. The objective was to understand how prompt design, structured reasoning, external tools, and retrieved knowledge influence the behavior and reliability of a large language model in a customer support environment.

The four techniques implemented were K-Shot Prompting, Chain-of-Thought Prompting, Tool Calling, and Retrieval-Augmented Generation (RAG). Each implementation was evaluated using the provided automated checks.

## 2. K-Shot Prompting — Ticket Classification

**File:** `k_shot_prompting.py`

### Objective

Classify incoming customer support messages into four categories: `billing`, `shipping`, `returns`, or `technical`. The model must return exactly one lowercase category label without additional explanations.

### Final System Prompt

```text
You are a customer support ticket classifier for an online store.

Classify each customer message into exactly one of these four categories:
billing, shipping, returns, technical.

Examples:
Message: I was charged the wrong amount.
Label: billing

Message: My delivery has not arrived yet.
Label: shipping

Message: Can I exchange the jacket I purchased?
Label: returns

Message: The website shows an error when I log in.
Label: technical

Respond with only the category label in lowercase.
Do not include explanations, punctuation, or additional text.
Do not output any label outside the four allowed categories.
```

### Sample Input and Output

**Input:**

```text
My card was charged twice for order 4412.
```

**Output:**

```text
billing
```

**Test result:** 4/4 correct.

### What I Learned

Providing labeled examples helped establish both the classification categories and the required output format. K-shot prompting allowed the model to perform a structured classification task without additional training or changes to the model itself. Restricting the output to the four categories specified in the assignment also demonstrated the importance of aligning prompt instructions with task requirements.

## 3. Chain-of-Thought Prompting — Refund Eligibility

**File:** `chain_of_thought.py`

### Objective

Determine refund eligibility based on the store's refund policy. The model must evaluate the purchase date, product condition, and final-sale status, then finish with an explicitly formatted decision.

### Final System Prompt

```text
You are a refund eligibility assistant for an online store.

Evaluate each refund request using the refund policy provided below.

Follow these steps in your response:
1. Check whether the purchase was made within the last 30 days.
2. Check whether the item is unused and in its original condition.
3. Check whether the item was marked as final sale.
4. Briefly explain which conditions are satisfied or violated.
5. Approve the refund only if all three requirements are satisfied.

If any requirement is violated, the refund must be denied.
If required information is missing, do not assume eligibility.

Your final line MUST be exactly one of the following:
DECISION: YES
DECISION: NO

Do not write anything after the final decision line.
```

The store's refund policy was provided separately in the program and appended to the system prompt.

### Sample Input and Output

**Input:**

```text
Bought 10 days ago, unused, not final sale.
```

**Observed model response:**

```text
1. The purchase was made within the last 30 days, so this requirement is satisfied.
2. The item is unused, so this requirement is satisfied.
3. The item was not marked as final sale, so this requirement is satisfied.

All three requirements are satisfied.

DECISION: YES
```

**Test result:** 3/3 correct.

### What I Learned

Breaking a policy decision into explicit evaluation steps made the task more systematic. Requiring a fixed final decision format also made the response easier for the program to validate.

Additional inspection of the model's complete responses showed that correct final decisions do not always guarantee fully consistent explanations. In the rejection scenarios, the model occasionally confused missing information with an unsatisfied requirement or made assumptions about an item's condition. This demonstrated the importance of evaluating both the final answer and its supporting explanation.

## 4. Tool Calling — Order Status Lookup

**File:** `tool_calling.py`

### Objective

Enable the model to identify an order number in a customer message and request the appropriate external function, `get_order_status`, rather than inventing an order status.

### Final System Prompt

```text
You are a helpful customer support assistant for an online store.

When a customer asks about an order:
1. Identify the exact order ID in the customer's message.
2. Call the get_order_status tool using that order ID as a string.
3. Do not guess or invent an order status.
4. Use the tool's result to provide a short, accurate response when the result is available.

Always use get_order_status before answering an order status question.
```

### Tool Definition

The tool schema described `get_order_status` as a function for retrieving a customer's current order status. Its required parameter, `order_id`, was defined as a string containing the exact order number extracted from the message.

### Sample Input and Output

**Input:**

```text
Hi, can you check on order 4412 for me?
```

**Model-generated tool call:**

```text
get_order_status(order_id="4412")
```

**Tool execution result:**

```text
shipped, arriving Friday
```

**Test result:** PASS — the model requested the tool with the correct order ID.

### What I Learned

Tool calling allows a language model to connect natural-language requests to external functions and structured data. The tool schema helps specify when the function should be used and which arguments it requires. In this implementation, the test verified the tool-call request and its argument; it did not implement a second model response after returning the tool result.

## 5. Retrieval-Augmented Generation (RAG) — Help-Center Answers

**File:** `rag.py`

### Objective

Answer customer questions using only information from `data/help_center.txt`. If the requested information is absent, the model must acknowledge that it does not know rather than generate an unsupported answer.

### Final System Prompt

```text
You are a customer support assistant for an online store.

Answer customer questions using ONLY the information provided in the Context section.

Rules:
1. Read the provided context carefully.
2. Answer only with facts explicitly supported by the context.
3. Do not use outside knowledge or make assumptions.
4. If the context is empty or does not contain the answer, politely say:
   "I don't know based on the available help-center information."
5. Keep your response short, clear, and helpful.
6. Never invent policies, shipping details, personal information, or other facts.
```

### Retrieval Approach

A lightweight keyword-based retriever was implemented in `YOUR_RETRIEVER`. The function checks the customer's question for topic-specific keywords related to returns, shipping, billing, warranty, and support.

It then selects help-center lines whose category matches the detected topic. Only those retrieved lines are included in the context supplied to the language model.

The billing keyword list was extended to include Visa, Mastercard, PayPal, and card-related terms. This improvement ensures that payment-method questions retrieve the relevant help-center information, even when the customer does not explicitly mention billing or payment.

This approach demonstrates the retrieval and answer-generation stages of RAG without requiring embeddings or a vector database.

### Sample Input and Output

**Input:**

```text
How long do I have to return an item?
```

**Output:**

```text
you have 30 days from delivery to return an item.
```

An additional test asked:

**Input:**

```text
What's your CEO's home address?
```

**Output:**

```text
i don't know based on the available help-center information.
```

**Test result:** 3/3 correct.

### What I Learned

RAG helped constrain the model's answers to information supplied by an external document. The retriever determined which information was available to the model, while the system prompt established rules against unsupported claims. The unknown-information test demonstrated the importance of explicitly instructing the model to acknowledge missing evidence.

## 6. Evaluation Summary

| Technique | Primary Mechanism | Test Result |
|---|---|---|
| K-Shot Prompting | Labeled examples and output constraints | 4/4 correct |
| Chain-of-Thought Prompting | Step-by-step policy evaluation | 3/3 correct |
| Tool Calling | Function schema and structured arguments | PASS |
| RAG | Keyword retrieval and context-grounded responses | 3/3 correct |

All four techniques passed their provided automated checks using the locally hosted `llama3.1:8b` model.

## 7. Overall Reflection — What I Learned

Across these four techniques, I learned that large language models are effective at structured tasks when the expected behavior is clearly specified. K-shot prompting uses examples to communicate patterns and output formats, while chain-of-thought prompting provides an explicit sequence for evaluating multiple conditions. However, prompts alone are not always sufficient for reliable real-world applications.

Tool calling provides a way to obtain information from external systems, and RAG supplies relevant documentary evidence while limiting unsupported answers. Together, these techniques demonstrate that effective LLM applications depend not only on the model's capabilities but also on carefully designed instructions, structured interfaces, retrieval mechanisms, and validation.

Passing the provided tests confirms the required behavior for the tested examples, but broader reliability would require additional cases and evaluation.
