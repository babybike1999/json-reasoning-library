# Eloquent JavaScript Reasoning OS — Assistant Start Here (v1)

## What this package is

This package converts the uploaded lawful copy of **Eloquent JavaScript, 4th edition, by Marijn Haverbeke** into a source-traceable reasoning library for JavaScript and practical internal tools, especially Google Apps Script projects.

It is not a book summary, exercise-solution manual, code-copy archive, current Apps Script reference, or replacement for the source book. Concepts, examples, and project lessons are paraphrased; no long passages, long code listings, full exercise solutions, or full project implementations are reproduced.

**Central rule:** JavaScript language reasoning transfers. Runtime assumptions do not automatically transfer.

## Authority order

1. Current project code and runtime behavior
2. Current error logs, execution logs, stack traces, and user reports
3. Current Google Apps Script documentation
4. Current Google Workspace service documentation
5. Current browser and Node.js documentation when relevant
6. Current business requirements, SOPs, and workflow rules
7. Source-supported JavaScript concepts from Eloquent JavaScript
8. Cross-chapter synthesis from the source
9. Google Apps Script translation-layer extensions
10. AI-agent workflow extensions
11. General programming advice

The source never overrides observed runtime behavior. When documentation and observed behavior appear to disagree, capture the exact code version, deployment, identity, input, log, and current documentation before changing a live tool.

## Runtime boundary matrix

| Concern | JavaScript language | HTMLService client | Server-side `.gs` | Node.js comparison |
|---|---|---|---|---|
| Values, operators, functions, scope, closures, objects, arrays | Strong conceptual transfer | Yes | Yes, subject to current V8 support | Yes |
| DOM, browser events, form elements, `window`, `document` | Host APIs, not language | Client only, subject to current HTMLService/browser behavior | **No** | Not normal server APIs |
| Browser promises and `fetch` | Language/API concepts | Client only when currently supported | Do not assume browser behavior | Node behavior differs by version/runtime |
| `google.script.run` | Not in the book | Async client-to-server boundary | Invokes server functions | Not a Node API |
| `SpreadsheetApp`, `DriveApp`, mail, properties, cache, locks | Not in the book | Call through server boundary | Apps Script services; verify current contracts | Not Node APIs |
| Filesystem, Node HTTP server, streams, NPM/CommonJS | Conceptual comparison only | Do not assume | Do not assume | Node-specific; verify current Node version |
| Quotas, triggers, scopes, permissions, deployment | Host behavior | Verify where relevant | Always current-verification territory | Runtime/provider-specific |

## Apps Script reasoning gate

1. What problem is the script solving?
2. What code runs client-side and what runs server-side?
3. What JavaScript concept is involved?
4. What Apps Script service or runtime behavior is involved?
5. What input shape is expected?
6. What validation happens before transformation?
7. What side effects happen, and when?
8. What could fail silently?
9. What error should the user see?
10. What should be logged for the developer?
11. Is there a dry-run path before live write?
12. What happens on partial failure?
13. What current Google documentation must be verified?
14. What test proves this works?

## Recommended workflow shape

`identify runtime → ingest → parse → validate → normalize → transform → reconcile → build action plan → dry run → authorize live effects → execute effects → verify destination → record run history → report status`

Keep service calls, file creation, mail, range writes, and external API effects outside row-level transformation helpers. A dry run should render the same action plan that live mode executes; it must not use a second transformation path.

## Error and status rules

Expected user/data problems should normally become structured validation results. Unexpected invariant or dependency failures should propagate to a boundary that can preserve the cause, record a safe diagnostic ID, report partial effects, and give the user a plain-language next action.

Never reduce mixed outcomes to one boolean. Distinguish at least: accepted, rejected, skipped, completed, failed, unknown outcome, and retryable. A retry needs a stable business-operation key; an execution ID alone is not idempotency.

## Current-verification triggers

Always verify current behavior for Apps Script V8 support; quotas and limits; triggers; deployments; authorization scopes and execution identity; HTMLService; `google.script.run`; uploads; SpreadsheetApp; DriveApp; UrlFetchApp; PropertiesService; CacheService; LockService; mail services; browser DOM/fetch/CORS; Node.js/NPM/modules; date/timezone behavior; external APIs; report schemas; and current project code, logs, settings, and SOPs.

The package was built under a source-only rule. No current Google, browser, Node, R365, provider, or project documentation was used to assert platform behavior.

## Which file to load

| Need | Primary file |
|---|---|
| Compact routing and gates | `eloquent_javascript_assistant_context_v1.json` |
| Source metadata, chapters, sections, pages, exercises, projects | `eloquent_javascript_source_map_v1.json` |
| Full combined reasoning OS | `eloquent_javascript_reasoning_os_full_v1.json` |
| Values/types/coercion | `eloquent_javascript_values_types_operators_v1.json` |
| Functions/scope/closures | `eloquent_javascript_functions_scope_closures_v1.json` |
| Objects/arrays/JSON/row shapes | `eloquent_javascript_data_structures_objects_arrays_v1.json` |
| Errors/testing/debugging | `eloquent_javascript_bugs_errors_testing_debugging_v1.json` |
| Regex/date parsing | `eloquent_javascript_regular_expressions_v1.json` |
| Async/client callbacks | `eloquent_javascript_async_programming_v1.json` |
| Browser/DOM/events | `eloquent_javascript_browser_dom_events_v1.json` |
| HTTP/forms/uploads | `eloquent_javascript_http_forms_v1.json` |
| Node comparison | `eloquent_javascript_node_runtime_v1.json` |
| Google Apps Script translation | `eloquent_javascript_google_apps_script_translation_layer_v1.json` |
| Internal-tool applications | `eloquent_javascript_internal_tools_workflows_v1.json` |
| Reusable risks | `eloquent_javascript_failure_modes_and_pitfalls_v1.json` |
| Concrete design choices | `eloquent_javascript_decision_rules_v1.json` |
| Evidence-seeking questions | `eloquent_javascript_diagnostic_questions_v1.json` |
| Review workflows | `eloquent_javascript_ai_agent_workflows_v1.json` |
| Time-sensitive claims | `eloquent_javascript_current_verification_flags_v1.json` |
| Validation and limitations | `eloquent_javascript_validation_manifest_v1.json` |
| Final file hashes | `eloquent_javascript_checksums_v1.sha256.json` |

## Source facts and limits

- Source: **Eloquent JavaScript, 4th edition, Marijn Haverbeke**; copyright/publication year shown: **2024**.
- The PDF has **435 pages**. All pages rendered; PDF p. 1 is the image-only cover, and the remaining pages have extractable text.
- Detected **21 numbered chapters**, **286 embedded-outline sections**, **135 additional typographic subheadings**, **60 titled exercises**, **56 exercise-hint headings**, and **5 project chapters**.
- ISBN is not explicitly labeled in the uploaded source. A numeric purchase-URL identifier was not treated as a verified ISBN.
- Technical counts of monospaced clusters, raster images, and vector drawings are not exact semantic counts of examples, figures, diagrams, or tables.
- Applied Apps Script, internal-tool, and cross-domain records are marked as extensions; they do not claim that the book discusses those systems.

## Completion standard for future assistants

A recommendation is not complete until it names the runtime, input and output shapes, validation, side effects, silent-failure paths, user message, developer diagnostics, dry-run/live behavior, partial failure, current-verification needs, and a test oracle. For live changes, also identify deployed version, permissions/identity, rollback, and post-deploy verification.
