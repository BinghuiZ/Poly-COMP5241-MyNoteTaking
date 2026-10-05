---
name: python-minimal-openrouter
description: Minimal Python changes for OpenRouter API code while preserving existing conversation and reasoning data.
---

# Minimal Python OpenRouter Changes

- Read the relevant file before editing.
- Make the smallest possible patch.
- Do not change unrelated code.
- Preserve the existing API style unless migration is requested.
- Preserve `reasoning_details` exactly as returned.
- Preserve `tool_calls` and other required assistant-message fields.
- Never stringify, summarize, reorder, filter, or reconstruct reasoning details.
- Do not change the model or reasoning settings unless requested.
- Do not add dependencies unless required.
- Do not refactor or reformat unrelated code.
- Inspect the final diff.
- Run only the narrowest relevant check.