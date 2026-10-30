## activate_skill

Activates a specialized agent skill by name (Available: 'skill-creator', 'antigravity-support'). Returns the skill's instructions wrapped in `<activated_skill>` tags. These provide specialized guidance for the current task. Use this when you identify a task that matches a skill's description. ONLY use names exactly as they appear in the `<available_skills>` section.

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "enum": [
        "skill-creator",
        "antigravity-support"
      ],
      "description": "The name of the skill to activate."
    }
  },
  "required": [
    "name"
  ],
  "additionalProperties": false,
  "$schema": "http://json-schema.org/draft-07/schema#"
}
```

## ask_user

Ask the user one or more questions to gather preferences, clarify requirements, or make decisions. When using this tool, prefer providing multiple-choice options with detailed descriptions and enable multi-select where appropriate to provide maximum flexibility.

```json
{
  "type": "object",
  "required": [
    "questions"
  ],
  "properties": {
    "questions": {
      "type": "array",
      "minItems": 1,
      "maxItems": 4,
      "items": {
        "type": "object",
        "required": [
          "question",
          "header",
          "type"
        ],
        "properties": {
          "question": {
            "type": "string",
            "description": "The complete question to ask the user. Should be clear, specific, and end with a question mark."
          },
          "header": {
            "type": "string",
            "description": "Very short label displayed as a chip/tag. Use abbreviations: \"Auth\" not \"Authentication\", \"Config\" not \"Configuration\". Examples: \"Auth method\", \"Library\", \"Approach\", \"Database\"."
          },
          "type": {
            "type": "string",
            "enum": [
              "choice",
              "text",
              "yesno"
            ],
            "default": "choice",
            "description": "Question type: 'choice' (default) for multiple-choice with options, 'text' for free-form input, 'yesno' for Yes/No confirmation with optional 'Other' feedback."
          },
          "options": {
            "type": "array",
            "description": "The selectable choices for 'choice' type questions. Provide 2-4 options. An 'Other' option is automatically added for 'choice' and 'yesno' types. Not needed for 'text' or 'yesno'.",
            "items": {
              "type": "object",
              "required": [
                "label",
                "description"
              ],
              "properties": {
                "label": {
                  "type": "string",
                  "description": "The display text for this option (1-5 words). Example: \"OAuth 2.0\""
                },
                "description": {
                  "type": "string",
                  "description": "Brief explanation of this option. Example: \"Industry standard, supports SSO\""
                }
              }
            }
          },
          "multiSelect": {
            "type": "boolean",
            "description": "Only applies when type='choice'. Set to true to allow selecting multiple options."
          },
          "placeholder": {
            "type": "string",
            "description": "Hint text shown in the input field. For type='text', shown in the main input. For type='choice' and 'yesno', shown in the 'Other' custom input."
          }
        }
      }
    }
  }
}
```

## enter_plan_mode

Switch to Plan Mode to safely research, design, and plan complex changes using read-only tools.

```json
{
  "type": "object",
  "properties": {
    "reason": {
      "type": "string",
      "description": "Short reason explaining why you are entering plan mode."
    }
  }
}
```

## glob

Efficiently finds files matching specific glob patterns (e.g., `src/**/*.ts`, `**/*.md`), returning absolute paths sorted by modification time (newest first). Ideal for quickly locating files based on their name or path structure, especially in large codebases.

```json
{
  "type": "object",
  "properties": {
    "pattern": {
      "description": "The glob pattern to match against (e.g., '**/*.py', 'docs/*.md').",
      "type": "string"
    },
    "dir_path": {
      "description": "Optional: The absolute path to the directory to search within. If omitted, searches the root directory.",
      "type": "string"
    },
    "case_sensitive": {
      "description": "Optional: Whether the search should be case-sensitive. Defaults to false.",
      "type": "boolean"
    },
    "respect_git_ignore": {
      "description": "Optional: Whether to respect .gitignore patterns when finding files. Only available in git repositories. Defaults to true.",
      "type": "boolean"
    },
    "respect_gemini_ignore": {
      "description": "Optional: Whether to respect .geminiignore patterns when finding files. Defaults to true.",
      "type": "boolean"
    }
  },
  "required": [
    "pattern"
  ]
}
```

## google_web_search

Performs a grounded Google Search to find information across the internet. Returns a synthesized answer with citations (e.g., [1]) and source URIs. Best for finding up-to-date documentation, troubleshooting obscure errors, or broad research. Use this when you don't have a specific URL. If a search result requires deeper analysis, follow up by using 'web_fetch' on the provided URI.

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "The search query. Supports natural language questions (e.g., 'Latest breaking changes in React 19') or specific technical queries."
    }
  },
  "required": [
    "query"
  ]
}
```

## grep_search

Searches for a regular expression pattern within file contents. Max 100 matches.

```json
{
  "type": "object",
  "properties": {
    "pattern": {
      "description": "The regular expression (regex) pattern to search for within file contents (e.g., 'function\\s+myFunction', 'import\\s+\\{.*\\}\\s+from\\s+.*').",
      "type": "string"
    },
    "dir_path": {
      "description": "Optional: The absolute path to the directory to search within. If omitted, searches the current working directory.",
      "type": "string"
    },
    "include_pattern": {
      "description": "Optional: A glob pattern to filter which files are searched (e.g., '*.js', '*.{ts,tsx}', 'src/**'). If omitted, searches all files (respecting potential global ignores).",
      "type": "string"
    },
    "exclude_pattern": {
      "description": "Optional: A regular expression pattern to exclude from the search results. If a line matches both the pattern and the exclude_pattern, it will be omitted.",
      "type": "string"
    },
    "names_only": {
      "description": "Optional: If true, only the file paths of the matches will be returned, without the line content or line numbers. This is useful for gathering a list of files.",
      "type": "boolean"
    },
    "max_matches_per_file": {
      "description": "Optional: Maximum number of matches to return per file. Use this to prevent being overwhelmed by repetitive matches in large files.",
      "type": "integer",
      "minimum": 1
    },
    "total_max_matches": {
      "description": "Optional: Maximum number of total matches to return. Use this to limit the overall size of the response. Defaults to 100 if omitted.",
      "type": "integer",
      "minimum": 1
    }
  },
  "required": [
    "pattern"
  ]
}
```

## invoke_agent

Invoke a subagent to perform a specific task or investigation.

```json
{
  "type": "object",
  "properties": {
    "agent_name": {
      "type": "string",
      "description": "Name of the subagent to invoke"
    },
    "prompt": {
      "type": "string",
      "description": "The COMPLETE query to send the subagent. MUST be comprehensive and detailed. Include all context, background, questions, and expected output format. Do NOT send brief or incomplete instructions."
    },
    "wait_for_previous": {
      "type": "boolean",
      "description": "Set to true to wait for all previously requested tools in this turn to complete before starting. Set to false (or omit) to run in parallel. Use true when this tool depends on the output of previous tools."
    }
  },
  "required": [
    "agent_name",
    "prompt"
  ]
}
```

## list_background_processes

Lists all active and recently completed background shell processes orchestrating by the agent.

```json
{
  "type": "object",
  "properties": {
    "wait_for_previous": {
      "type": "boolean",
      "description": "Set to true to wait for all previously requested tools in this turn to complete before starting. Set to false (or omit) to run in parallel. Use true when this tool depends on the output of previous tools."
    }
  }
}
```

## list_directory

Lists the names of files and subdirectories directly within a specified directory path. Can optionally ignore entries matching provided glob patterns.

```json
{
  "type": "object",
  "properties": {
    "dir_path": {
      "description": "The path to the directory to list",
      "type": "string"
    },
    "ignore": {
      "description": "List of glob patterns to ignore",
      "items": {
        "type": "string"
      },
      "type": "array"
    },
    "file_filtering_options": {
      "description": "Optional: Whether to respect ignore patterns from .gitignore or .geminiignore",
      "type": "object",
      "properties": {
        "respect_git_ignore": {
          "description": "Optional: Whether to respect .gitignore patterns when listing files. Only available in git repositories. Defaults to true.",
          "type": "boolean"
        },
        "respect_gemini_ignore": {
          "description": "Optional: Whether to respect .geminiignore patterns when listing files. Defaults to true.",
          "type": "boolean"
        }
      }
    }
  },
  "required": [
    "dir_path"
  ]
}
```

## read_background_output

Reads the output log of a background shell process. Support reading tail snapshot.

```json
{
  "type": "object",
  "properties": {
    "pid": {
      "type": "integer",
      "description": "The process ID (PID) of the background process to inspect."
    },
    "lines": {
      "type": "integer",
      "minimum": 1,
      "description": "Optional. Number of lines to read from the end of the log. Defaults to 100."
    },
    "delay_ms": {
      "type": "integer",
      "description": "Optional. Delay in milliseconds to wait before reading the output. Useful to allow the process to start and generate initial output."
    },
    "wait_for_previous": {
      "type": "boolean",
      "description": "Set to true to wait for all previously requested tools in this turn to complete before starting. Set to false (or omit) to run in parallel. Use true when this tool depends on the output of previous tools."
    }
  },
  "required": [
    "pid"
  ]
}
```

## read_file

Reads and returns the content of a specified file. To maintain context efficiency, you MUST use 'start_line' and 'end_line' for targeted, surgical reads of specific sections. For your safety, the tool will automatically truncate output exceeding 2000 lines, 2000 characters per line, or 20MB in size; however, triggering these limits is considered token-inefficient. Always retrieve only the minimum content necessary for your next step. Handles text, images (PNG, JPG, GIF, WEBP, SVG, BMP), audio files (MP3, WAV, AIFF, AAC, OGG, FLAC), and PDF files.

```json
{
  "type": "object",
  "properties": {
    "file_path": {
      "description": "The path to the file to read.",
      "type": "string"
    },
    "start_line": {
      "description": "Optional: The 1-based line number to start reading from.",
      "type": "integer",
      "minimum": 1
    },
    "end_line": {
      "description": "Optional: The 1-based line number to end reading at (inclusive).",
      "type": "integer",
      "minimum": 1
    }
  },
  "required": [
    "file_path"
  ]
}
```

## replace

Replaces text within a file. By default, the tool expects to find and replace exactly ONE occurrence of `old_string`. If you want to replace multiple occurrences of the exact same string, set `allow_multiple` to true. This tool is preferred for surgical edits to existing files as it minimizes token usage, simplifies code reviews, and avoids accidental deletions. This tool requires providing significant context around the change to ensure precise targeting.
The user has the ability to modify the `new_string` content. If modified, this will be stated in the response.

```json
{
  "type": "object",
  "properties": {
    "file_path": {
      "description": "The path to the file to modify.",
      "type": "string"
    },
    "instruction": {
      "description": "A clear, semantic instruction for the code change, acting as a high-quality prompt for an expert LLM assistant. It must be self-contained and explain the goal of the change.",
      "type": "string"
    },
    "old_string": {
      "description": "The exact literal text to replace, unescaped. If this string is not the exact literal text (i.e. you escaped it) or does not match exactly, the tool will fail.",
      "type": "string"
    },
    "new_string": {
      "description": "The exact literal text to replace `old_string` with, unescaped. Provide the EXACT text. Ensure the resulting code is correct and idiomatic. Do not use omission placeholders like '(rest of methods ...)', '...', or 'unchanged code'; provide exact literal code.",
      "type": "string"
    },
    "allow_multiple": {
      "type": "boolean",
      "description": "If true, the tool will replace all occurrences of `old_string`. If false (default), it will only succeed if exactly one occurrence is found."
    }
  },
  "required": [
    "file_path",
    "instruction",
    "old_string",
    "new_string"
  ]
}
```

## run_shell_command

This tool executes a given shell command as `powershell.exe -NoProfile -Command <command>`. To run a command in the background, set the `is_background` parameter to true. Do NOT use PowerShell background constructs.

      Efficiency Guidelines:
      - Quiet Flags: Always prefer silent or quiet flags (e.g., `npm install --silent`, `git --no-pager`) to reduce output volume while still capturing necessary information.
      - Pagination: Always disable terminal pagination to ensure commands terminate (e.g., use `git --no-pager`, `systemctl --no-pager`, or set `PAGER=cat`).

      The following information is returned:

      Output: Combined stdout/stderr. Can be `(empty)` or partial on error and for any unwaited background processes.
      Exit Code: Only included if non-zero (command failed).
      Error: Only included if a process-level error occurred (e.g., spawn failure).
      Signal: Only included if process was terminated by a signal.
      Background PIDs: Only included if background processes were started.
      Process Group PGID: Only included if available.

```json
{
  "type": "object",
  "properties": {
    "command": {
      "type": "string",
      "description": "Exact command to execute as `powershell.exe -NoProfile -Command <command>`"
    },
    "description": {
      "type": "string",
      "description": "Brief description of the command for the user. Be specific and concise. Ideally a single sentence. Can be up to 3 sentences for clarity. No line breaks."
    },
    "dir_path": {
      "type": "string",
      "description": "(OPTIONAL) The path of the directory to run the command in. If not provided, the project root directory is used. Must be a directory within the workspace and must already exist."
    },
    "is_background": {
      "type": "boolean",
      "description": "Set to true if this command should be run in the background (e.g. for long-running servers or watchers). The command will be started, allowed to run for a brief moment to check for immediate errors, and then moved to the background."
    },
    "delay_ms": {
      "type": "integer",
      "description": "Optional. Delay in milliseconds to wait after starting the process in the background. Useful to allow the process to start and generate initial output before returning."
    }
  },
  "required": [
    "command"
  ]
}
```

## update_topic

Manages your narrative flow. Include `title` and `summary` only when starting a new Chapter (logical phase) or shifting strategic intent.

```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "The title of the new topic or chapter."
    },
    "summary": {
      "type": "string",
      "description": "(OPTIONAL) A detailed summary (5-10 sentences) covering both the work completed in the previous topic and the strategic intent of the new topic. This is required when transitioning between topics to maintain continuity."
    },
    "strategic_intent": {
      "type": "string",
      "description": "A mandatory one-sentence statement of your immediate intent."
    },
    "wait_for_previous": {
      "type": "boolean",
      "description": "Set to true to wait for all previously requested tools in this turn to complete before starting. Set to false (or omit) to run in parallel. Use true when this tool depends on the output of previous tools."
    }
  },
  "required": [
    "strategic_intent"
  ]
}
```

## web_fetch

Analyzes and extracts information from up to 20 URLs. Ideal for documentation review, technical research, or reading raw code from GitHub. You can provide specific, complex instructions for the extraction (e.g., 'Summarize the breaking changes'). Provides cited answers based on the content. GitHub 'blob' URLs are automatically converted to raw versions for better processing. Supports HTTP/HTTPS only.

```json
{
  "type": "object",
  "properties": {
    "prompt": {
      "description": "A string containing the URL(s) and your specific analysis instructions. Be clear about what information you want to find or summarize. Supports up to 20 URLs.",
      "type": "string"
    }
  },
  "required": [
    "prompt"
  ]
}
```

## write_file

Writes the complete content to a file, automatically creating missing parent directories. Overwrites existing files. The user has the ability to modify 'content' before it is saved. Best for new or small files; use 'replace' for targeted edits to large files to minimize token usage and simplify reviews.

```json
{
  "type": "object",
  "properties": {
    "file_path": {
      "description": "Path to the file.",
      "type": "string"
    },
    "content": {
      "description": "The complete content to write. Provide the full file; do not use placeholders like '// ... rest of code'.",
      "type": "string"
    }
  },
  "required": [
    "file_path",
    "content"
  ]
}
```

