# Week 1 — Environment Setup

**GitHub username:** Rxd3

## My setup

I use Windows, PowerShell, and Visual Studio Code. My installed tools were checked on October 9, 2026:

- Git: 2.50.0.windows.1
- GitHub CLI: 2.102.0
- Visual Studio Code: 1.141.0
- OpenAI Codex VS Code extension: 26.1002.51308
- Python: 3.13.5 by default, with 3.12.4 also installed

I chose Codex because I can use it directly in VS Code and review its changes there.

## Setup checks

I checked the tool versions and confirmed that my Git name and email are configured. `gh auth status` confirmed that I am signed in as `Rxd3`.

`python --version` shows 3.13.5, while `py -3.12 --version` shows 3.12.4. This meets the assignment's Python 3.12 installation requirement.

For my earlier Codex demonstration, I asked it to create a Python temperature converter and reviewed the code. The saved version in Git history was checked again with Python 3.12.4. It correctly converted 0°C to 32°F and 32°F to 0°C.

## My contribution

I opened [pull request #70](https://github.com/scottyUX/AI-Augmented-Software-Engineering/pull/70) from `clarify-windows-pr-command`, using commit `c0399d3`.

I added a single-line `gh pr create` example to the Week 1 assignment for PowerShell users and cleaned up some Markdown spacing. This makes the instructions easier to follow on Windows. The PR is open for review.

## Issues and lessons

PowerShell initially did not recognize `gh`. It now works, and authentication was verified.

The `codex` command was also initially missing. I use the VS Code extension, so a separate CLI installation is optional. During the latest check, the extension's bundled command reported `codex-cli 0.162.0-alpha.2`.

I learned to check tool versions, test AI-generated code, and use a branch and pull request for changes. I also learned that Git does not automatically sync local changes with GitHub.

I reviewed the Week 1, Week 2, and Week 3 assignment instructions to understand the course workflow and identify opportunities for improvement. I also applied for the GitHub Student Developer Pack; my application is accepted.
