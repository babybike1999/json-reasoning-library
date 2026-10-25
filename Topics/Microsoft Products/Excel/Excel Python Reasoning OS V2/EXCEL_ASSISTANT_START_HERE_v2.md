# Excel + Python-in-Excel Assistant Package v2

Created: 2026-06-19T22:19:55Z

This is a focused v2 repair pass, not a rebuild from scratch. It keeps the useful v1 concepts, removes repeated boilerplate, compresses generic warnings into reusable risk records, and separates source-supported guidance from operational extensions.

## Use these files first

1. `excel_python_assistant_context_v2.json` - compact active-use context for AI agents.
2. `excel_agent_workbook_safety_pack_v2.json` - reusable risk records, gates, workflows, and architecture patterns.
3. `excel_vs_python_decision_rules_v2.json` - choose Excel, Python-in-Excel, Power Query, or external Python.
4. `excel_ai_agent_workflows_v2.json` - step-by-step workbook inspection, validation, repair, and rollback workflows.
5. `excel_business_operations_applications_v2.json` - restaurant/business reporting templates with policy placeholders.

## Non-negotiable workbook safety rules

- Inspect before modifying.
- Create a backup before edits.
- Preserve raw data and formula zones.
- Treat hidden sheets, external links, stale PivotTables, percent conventions, dates, blanks, and manual overrides as risks until checked.
- Do not invent company formulas, thresholds, mappings, accounting rules, API schema, or credentials.
- Use Python-in-Excel only when it improves the analysis and current availability/privacy constraints are verified.
- Use external Python or governed services for scheduled, credentialed, API-connected, or production workflows.

## Source-calibration note

The Excel book directly supports the Excel techniques around Tables, PivotTables, PivotCharts, data tables, Goal Seek, Scenario Manager, Solver, functions, statistics, forecasts, and Data Models. It did not provide a dedicated data-validation/governance chapter in the extracted text, so v2 data-quality gates and workbook-safety workflows are labeled as operational extensions. The Python-in-Excel book supports PY cells, the Python Editor, `xl()`, pandas/NumPy/visualization libraries, errors, Copilot examples, and Power Query handoff; current product behavior is covered by current-verification flags.
