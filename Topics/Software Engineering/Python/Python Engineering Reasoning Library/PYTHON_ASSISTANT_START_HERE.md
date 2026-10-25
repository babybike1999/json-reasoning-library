# Python Engineering Reasoning Library — Start Here

Generated: 2026-06-16T06:13:43+00:00

This package contains a reusable, source-separated reasoning library derived from the uploaded editions of **Robust Python** and **Architecture Patterns with Python**.

## Use this first in future coding chats

Upload `python_coding_assistant_context.json` and this file. Ask the coding assistant to follow the context before proposing architecture or refactors.

## Governing behavior for coding assistants

Inspect current code before recommending architecture. Use exact filenames and symbols. Preserve working behavior. Distinguish observed code from proposals. Add tests before material refactoring. Prefer incremental patches. Avoid speculative abstractions, microservices by default, and rewrites merely to match a pattern. State assumptions and what remains unverified. Never claim code was executed when it was not. Include rollback guidance. Keep secrets out of output. Verify current external documentation for time-sensitive library behavior. Apply source-derived patterns only when they solve a demonstrated problem.

## Source separation

- `robust_python_reliability_os_full.json` is the canonical Robust Python knowledge base.
- `architecture_patterns_python_os_full.json` is the canonical Architecture Patterns knowledge base.
- `python_reliability_architecture_integration_os.json` is the separate cross-book synthesis layer.
- `python_coding_assistant_context.json` is the compact future-chat context.

Cross-book records reference source record IDs from each book instead of pretending the books use identical terminology.

## Source limitation

The upload contained unpacked EPUB directories, not PDFs. Traceability therefore uses EPUB HTML filenames and anchors instead of page numbers. Code listings are inventoried by hash/length only; no long copyrighted code is reproduced.

## Recommended upload set for future chats

For small chats, upload `PYTHON_ASSISTANT_START_HERE.md` and `python_coding_assistant_context.json`. For deep design work, also upload the relevant full book JSON and the integration JSON.
