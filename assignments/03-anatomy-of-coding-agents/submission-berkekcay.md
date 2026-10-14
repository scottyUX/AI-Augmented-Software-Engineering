# Week 3 submission: Berke Eren Akçay

Repository: https://github.com/berkekcay/support-desk-prompting

All four starter checks pass with `llama3.1:8b` at temperature 0 (k-shot 4/4, chain of thought
3/3, tool calling PASS, RAG 3/3), and only the `TODO` parts were edited. With the empty starter
prompts the results were 0/4, 0/3, PASS and 2/3, and the two RAG passes were invented answers.

I also tried each prompt on inputs that aren't in the checks. That found a chain-of-thought bug
("I wore it once" was approved), which I fixed in the prompt, and a tool-calling case the prompt
couldn't fix (the model calls the tool with an empty order id). The final prompts, samples and
what I learned are in
[writeup.md](https://github.com/berkekcay/support-desk-prompting/blob/main/writeup.md).
