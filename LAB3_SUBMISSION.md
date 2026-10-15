# Lab 3 Submission: A Mini Coding Agent

**Student:** Hacer Dilara Kivrak

**Project Repository:** https://github.com/hacerdilarakivrak/lab3-mini-coding-agent

## Project Summary

I implemented a mini coding agent using Python, the OpenAI Python client, Ollama, and the `llama3.1:8b` language model.

The agent communicates with the locally running Ollama server through an OpenAI-compatible API.

The implementation includes an iterative agent loop and three tools:

- `list_files` — Lists files inside the project directory.
- `read_file` — Reads project files.
- `run_tests` — Runs Python unit tests after explicit user approval.

## Safety Features

- File access is restricted to the project directory.
- Tool names and arguments are validated before execution.
- Running tests requires explicit user approval.
- The agent loop is limited to 20 iterations.
- The project structure is included in the system prompt.
- Unknown tool calls are rejected.
- Test execution has a 30-second timeout.

## Test Results

- **Automated unit tests:** 12/12 PASS.
- **OpenAI-compatible API connection:** PASS.
- **Manual agent execution:** PASS.
- **File listing and reading:** PASS.
- **User permission control:** PASS (automated test).
- **20-iteration stopping condition:** PASS (automated test).

The automated tests were executed using:

`python -m unittest discover -v`

Test output:

```text
Ran 12 tests in 0.020s

OK
```

The agent was also tested manually using the `llama3.1:8b` model through the OpenAI-compatible API. It successfully listed project files, read documentation, and generated a project summary in two iterations.

## Documentation

The complete source code, tests, and documentation are available in the linked project repository.

- [README.md](https://github.com/hacerdilarakivrak/lab3-mini-coding-agent/blob/main/README.md)
- [writeup.md](https://github.com/hacerdilarakivrak/lab3-mini-coding-agent/blob/main/writeup.md)
- [mini_coding_agent.py](https://github.com/hacerdilarakivrak/lab3-mini-coding-agent/blob/main/mini_coding_agent.py)
- [test_mini_coding_agent.py](https://github.com/hacerdilarakivrak/lab3-mini-coding-agent/blob/main/test_mini_coding_agent.py)

## Reference Comparison

I compared my implementation with [rasbt/mini-coding-agent](https://github.com/rasbt/mini-coding-agent).

My implementation focuses on three essential coding tools and basic safety controls, while the reference project includes more advanced features such as persistent memory, session recovery, context management, and additional tool capabilities.

A detailed comparison is provided in `writeup.md`.
