# Agent Instructions

## Primary objective

Write only the minimum code required to satisfy the user's request.

Do not change code, files, formatting, behavior, APIs, dependencies, or configuration that the user did not explicitly ask to change.

## Before editing

1. Read the relevant existing files.
2. Inspect the current git diff.
3. Identify the exact requested behavior.
4. Identify the smallest possible patch.
5. State the intended change briefly before editing.
6. If the request is ambiguous, ask a question instead of guessing.

## Minimal-change rules

- Modify only the files necessary for the request.
- Preserve all unrelated code exactly as it is.
- Do not refactor unrelated code.
- Do not rename variables, functions, files, or APIs unless requested.
- Do not reformat unrelated lines.
- Do not reorder imports unless required.
- Do not add comments, type annotations, abstractions, helper functions, logging, validation, or documentation unless required.
- Do not add dependencies unless explicitly requested.
- Do not update dependency versions or lockfiles unless required.
- Do not fix unrelated bugs.
- Do not add speculative features.
- Do not create unused variables or placeholder code.
- Do not run broad formatters on a small change.
- Do not rewrite a complete file when a small patch is sufficient.

## Python rules

- Use the existing Python version and project style.
- Reuse existing functions and dependencies.
- Prefer the standard library when it is already sufficient.
- Preserve existing function signatures.
- Preserve existing exception behavior unless the user asks to change it.
- Keep the implementation as short as possible without reducing correctness.
- Do not add a class when a function is sufficient.
- Do not add a helper function when a direct change is sufficient.
- Do not add error handling that the user did not request.
- Do not change unrelated whitespace.

## OpenRouter rules

- Use the existing OpenRouter API structure unless the user asks for a migration.
- Preserve the user's selected model unless explicitly asked to change it.
- Preserve `reasoning_details` exactly as returned by OpenRouter.
- Do not edit, summarize, reorder, filter, or reconstruct `reasoning_details`.
- Preserve all relevant assistant-message fields when continuing a conversation.
- If the assistant message contains `tool_calls`, preserve them exactly when sending the message back.
- Do not expose private reasoning to the end user unless explicitly requested and permitted.
- Do not add reasoning output merely for display.
- Use `reasoning: {"enabled": true}` only when reasoning is required.
- Do not change reasoning settings, model, token limits, or routing without being asked.
- Keep API keys out of source code when editing production code.
- Prefer environment variables for secrets if the user requests security improvements.

## OpenRouter conversation continuity

When continuing a conversation, preserve the assistant response exactly enough for OpenRouter to validate it.

Minimum pattern:

```python
assistant_message = response["choices"]["message"]

messages = [
    original_user_message,
    {
        "role": "assistant",
        "content": assistant_message.get("content"),
        "reasoning_details": assistant_message.get("reasoning_details"),
    },
    follow_up_user_message,
]
```

If the assistant message contains additional fields required by the API, preserve them too.

Do not do this:

```python
reasoning_details = str(assistant_message["reasoning_details"])
```

Do not do this:

```python
reasoning_details = assistant_message["reasoning_details"][-1:]
```

Do not do this:

```python
reasoning_details = sorted(assistant_message["reasoning_details"])
```

The complete sequence must remain unchanged.

## Editing procedure

1. Explain the proposed minimal change.
2. Edit only the necessary lines.
3. Inspect the resulting diff.
4. Remove any unrelated changes.
5. Run the narrowest relevant check.
6. Report:
   - files changed,
   - concise description of the change,
   - checks run,
   - anything not verified.

## Stop and ask before proceeding

Ask for confirmation if:

- Another file must be changed unexpectedly.
- A dependency must be added or upgraded.
- A public API must change.
- A database schema must change.
- A broad refactor appears necessary.
- The existing code and user request conflict.
- The requested behavior is ambiguous.
- The change could delete or overwrite user data.

## Neon database rules

- Use the official Neon skill and MCP server when working with Neon.
- Do not modify the database schema unless the user explicitly requests it.
- Before any schema change, show the exact SQL and explain its effect.
- Never drop tables, columns, indexes, branches, or databases without explicit confirmation.
- Never run destructive SQL automatically.
- Do not change migrations that the user did not mention.
- Do not create a new migration for a code-only change.
- Do not change application code when the request only concerns the database.
- Do not change the database when the request only concerns application code.
- Inspect the current schema before proposing SQL.
- Reuse existing tables, columns, indexes, and migrations where possible.
- Make the smallest database change that satisfies the request.
- Preserve existing naming conventions.
- Do not add seed data, test data, triggers, policies, or indexes unless requested or required.
- After a change, report the exact SQL or migration file changed.

## Web UI design rules

- Inspect the current UI before editing.
- Do not redesign the page unless explicitly requested.
- Preserve the current layout, components, routes, content, and behavior.
- Make only the smallest changes needed to fix the identified issue.
- Do not change unrelated CSS, HTML, JavaScript, TypeScript, or configuration.
- Do not replace the UI framework or styling system.
- Do not add a dependency unless explicitly requested.
- Do not change colors, fonts, spacing, breakpoints, or component structure unless the request requires it.
- Do not apply broad formatting or CSS cleanup.
- Do not fix unrelated accessibility or design issues.
- Before editing, list the exact files and UI issues to be changed.
- After editing, inspect the diff and verify the affected viewport.
- Ask for confirmation before changing more files than originally identified.