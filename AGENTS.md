# Agent Guidelines

## MCP Tool Usage

### context7
Use `context7` when you need to look up documentation for a library, framework,
or tool. Prefer this over guessing API shapes or relying on training knowledge
for versioned APIs.

Examples of when to use it:
- Looking up the correct signature for a framework method
- Checking the latest config options for a tool
- Verifying deprecated vs current API usage

### gh_grep
Use `gh_grep` when you need real-world usage examples from codebases on GitHub.
Only invoke it when context7 doesn't cover the use case or when you need to see
how something is used in practice.

Examples of when to use it:
- Finding patterns for an uncommon or niche integration
- Seeing how others structure a specific type of file or module
- Verifying an approach when docs are sparse

## General Rules
- Do not invoke MCP tools speculatively. Only call them when the information
  is actually needed to complete the task.
- Prefer context7 over gh_grep when both could answer the question — it uses
  fewer tokens.
- Do not call the same MCP tool more than once for the same question in a session.
