---
name: python-minimal-code
description: Write or modify Python code with the smallest possible patch. Use when implementing, fixing, refactoring, or reviewing Python code.
---

# Python Minimal Code

## Core rules

- Read the relevant existing files before writing code.
- First identify the exact user-requested behavior.
- Make the smallest change that satisfies the request.
- Do not rewrite, reformat, rename, reorganize, or optimize unrelated code.
- Do not add abstractions, helper functions, comments, documentation, logging, validation, typing, dependencies, or tests unless they are required by the request or the existing project conventions.
- Preserve existing behavior outside the requested change.
- Preserve the existing coding style.
- Do not change public APIs, function signatures, file names, imports, configuration, or dependency versions unless explicitly requested.
- Do not modify generated files unless explicitly requested.
- Do not fix unrelated bugs.
- Do not use broad search-and-replace.
- Do not create placeholder code, unused variables, speculative code, or unnecessary defensive checks.

## Before editing

1. Inspect the relevant files and nearby code.
2. Check the current git diff.
3. Determine the smallest file and smallest code region that must change.
4. State the intended minimal change in one sentence.
5. If the request is ambiguous or requires unrelated changes, ask before editing.

## While editing

- Edit only the files necessary for the request.
- Prefer a small targeted patch.
- Keep existing code unchanged whenever possible.
- Do not run formatters that may rewrite unrelated files.
- Do not update lockfiles or dependencies unless required.

## After editing

- Inspect the diff.
- Confirm every changed line is related to the request.
- Run only the narrowest relevant test or check.
- If a check modifies unrelated files, revert those unrelated modifications.
- Report changed files, tests run, and anything not verified.

## Stop conditions

Stop and ask for confirmation if:

- The requested behavior cannot be implemented without changing unrelated code.
- The change requires a new dependency.
- A public API must change.
- Existing tests contradict the request.
- The task requires a broad refactor.
- You find unrelated problems.