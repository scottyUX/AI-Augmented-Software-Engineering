---
trigger: glob
globs: tests/**
---

When reading or editing any file under `tests/`, follow the rules in `tests/AGENTS.md`:
public-API-only tests via the `client` fixture, success + failure coverage, independent
tests with a fresh database each, and assertions on observable behavior.
