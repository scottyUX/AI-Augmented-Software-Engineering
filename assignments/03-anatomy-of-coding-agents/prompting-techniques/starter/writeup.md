# Week 3 — Prompting Techniques Writeup

## 1. K-shot Prompting

### Final prompt

```text
You are a customer support message classifier.

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
```

### Sample input and output

**Input:** `My card was charged twice for order 4412.`

**Output:** `billing`

### What I learned

When no examples are provided, there can be many unclear points in the task, and the model may not fill in those gaps in the way I have in mind. When I provide examples that show exactly what I mean, the result is more successful. Without the output rules, the model could give a long answer, use uppercase letters, or add its own comments.

## 2. Chain-of-Thought Prompting

### Final prompt

```text
You are a bot that checks refund conditions. I want you to determine whether the product is eligible for a refund.

Check the following three conditions in order:

1. Was the product purchased within 30 days?
2. Is the product unused and in its original condition?
3. Is the product a final-sale item?

For each condition, write the result of your check and a short reason on a separate line.

Use only the provided refund policy and order information. Do not perform any checks or make any assumptions outside the policy.

The final line of your answer must be exactly one of these two options:

DECISION: YES
DECISION: NO

Do not add any other words, explanations, or punctuation to the final decision line.
```

### Sample input and output

**Input:** `Bought 10 days ago, unused, not final sale.`

**Output:**

```text
1. Was the product purchased within 30 days? Result: YES
The product was bought 10 days ago, which is within the 30-day timeframe.

2. Is the product unused and in its original condition? Result: YES
The product is unused and in its original condition.

3. Is the product a final-sale item? Result: NO
The product is not a final-sale item.

DECISION: YES
```

### What I learned

If the model only says yes or no, it may have evaluated something incorrectly and I would not notice it. The model can sometimes overlook a condition, but checking each condition separately makes the mistake easier to find and gives the model a chance to catch it. Using an exact yes-or-no decision format also removes the need for further interpretation; otherwise, the result could remain open to different interpretations.

## 3. Tool Calling

### Final prompt and tool descriptions

```text
Tool description:
Looks up the status of an order. Use it when a customer asks about an order's status or delivery. The customer's order number must be provided when calling the tool.

order_id description:
The order number found in the customer's message. Use the number exactly as it appears in the message.

System prompt:
When a customer asks about an order's status or delivery, use the get_order_status tool.

Find the order number in the customer's message and call the tool with that number.

Do not guess or invent an order status.

If the customer does not provide an order number, do not guess one; ask the customer for the order number.

Do not produce an answer about the order status before receiving the tool's result.

Use the result returned by the tool to give the customer a short and clear answer.
```

### Sample input and output

**Input:** `Hi, can you check on order 4412 for me?`

**Tool call:** `get_order_status(order_id="4412")`

**Tool result:** `shipped, arriving Friday`

**Output:** `Order 4412 has shipped and is arriving Friday.`

### What I learned

The model could make an incorrect assumption or guess, while using the tool makes the order status certain. If the tool and `order_id` descriptions were not clear, the model might not understand when to use the tool or could send the wrong information instead of the order number from the customer's message.

## 4. Retrieval-Augmented Generation (RAG)

### Final prompt

```text
You are a customer support bot.

Use the provided context to answer the customer's question. Find the necessary information in the context and give an appropriate answer to the customer.

Use only the information in the provided context when answering.

If the answer to the question is not in the context, reply exactly: I do not know based on the provided information.

Do not use your own knowledge outside the context.

Do not invent information or make guesses or assumptions.

Keep your answer short and clear.
```

### Retriever approach

The retriever normalizes the words in the question and help-center chunks, removes common words, and matches identical words or related word forms such as `return/returns`, `ship/shipping`, and `international/internationally`. It sends only the matching help-center lines to the model as context.

### Sample input and output

**Input:** `How long do I have to return an item?`

**Retrieved context:** `Returns: You may return most items within 30 days of delivery for a full refund.`

**Output:** `You may return most items within 30 days of delivery for a full refund.`

**Unsupported input:** `What's your CEO's home address?`

**Retrieved context:** Empty

**Output:** `I do not know based on the provided information.`

### What I learned

My graduation project was also based on RAG, and we used it in the field of psychology. A model can hallucinate, and grounding it in written information helps us prevent that. The same principle applies when writing code: we need to think about every possible state. It is not enough to define only the successful case; there can also be failure cases or ambiguous situations, and we need to make all of them clear.

## Closing Reflection

AI does not think in the same way as a human and does not automatically share the unstated context in our minds. We first need to understand how to communicate with it before we can assign it a task effectively. The reason we achieved a higher success rate in these four exercises was that we showed the model exactly what we wanted and, when the task was complex, clearly described the steps it should follow without leaving important points ambiguous. Providing examples together with the expected outputs was also especially effective. Models therefore perform well on structured tasks when they receive clear goals, steps, formats, tools, and grounded information, but they need additional scaffolding when a task is ambiguous, complex, dependent on external facts, or has failure cases that must be handled explicitly.
