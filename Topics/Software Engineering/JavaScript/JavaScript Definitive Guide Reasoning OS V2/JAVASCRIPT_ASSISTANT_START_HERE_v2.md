# JavaScript Reasoning OS V2 - Start Here

This V2 repair package is a focused cleanup of the existing JavaScript Reasoning OS. It does not overwrite the previous package. It uses the uploaded book source as the authority for JavaScript language, browser, Node, and tooling topics as covered in the source, and marks current platform/tooling behavior for verification.

## Authority order

1. Original uploaded book source: *JavaScript: The Definitive Guide, Seventh Edition* by David Flanagan.
2. Current generated JavaScript Reasoning OS package as a draft, not final truth.
3. Repair prompt requirements.
4. Current official documentation only when available and checked.
5. General engineering reasoning.

## Fast-use files

- `javascript_assistant_context_v2.json`: compact active context for an AI reviewer.
- `javascript_core_language_concepts_v2.json`: source-labeled language semantics plus reusable risk records.
- `javascript_pitfalls_and_failure_modes_v2.json`: strongest failure-mode file; start here for debugging.
- `javascript_diagnostic_questions_v2.json`: concrete questions for code review and bug triage.
- `javascript_code_review_workflows_v2.json`: 21 practical review workflows.
- `javascript_api_and_runtime_boundary_registry_v2.json`: separates ECMAScript, browser, Node, tooling, and Apps Script.
- `javascript_current_verification_flags_v2.json`: lists current-doc checks and affected record IDs.

## Non-negotiable runtime rules

- ECMAScript language features are not the same as browser APIs, Node APIs, tooling behavior, or Apps Script services.
- Browser APIs such as `document`, DOM events, browser storage, and browser workers are not assumed in Node.
- Node APIs such as `fs`, `process`, streams, HTTP server APIs, child processes, and worker_threads are not assumed in browsers.
- Google Apps Script is an operational extension. Do not treat server-side `.gs` files, HtmlService client HTML, triggers, and Apps Script services as ordinary browser or Node code.
- Current browser, Node, npm, bundler, Babel, JSX, Flow, ESLint, Prettier, Jest, deployment, security, and Apps Script claims require current official documentation before being asserted.

## JavaScript failure-mode checklist

1. Nullish access: Which value could be `null` or `undefined` before property access, element access, destructuring, or call?
2. Coercion: Which comparison, arithmetic operation, string concatenation, truthiness check, object-to-primitive conversion, or JSON conversion depends on implicit conversion?
3. Mutation: Which object or array is mutated through a shared reference?
4. Arrays: Could the array be sparse, array-like, or mutated during iteration?
5. `this`: Which functions depend on `this`, and how are they invoked?
6. Closures: Which variables are captured and can change before the callback runs?
7. Prototypes/classes: Is the property own or inherited? Is a method on the prototype or per instance?
8. Modules: Which module system and loader execute this file?
9. Async: Which Promise rejection path is handled? Which async operation must finish before returning? Which callback error channel is tested?
10. Data boundaries: Which JSON values are lost? Which date/time assumption depends on timezone? Which regex negative tests prevent overmatching?
11. Runtime: Which browser API is unavailable in Node? Which Node API is unavailable in the browser? Which Apps Script service/API needs current Google docs?
12. Tooling: Is the code reviewed the same code executed after bundling/transpilation/tests?

## Async review standard

Do not give generic "use async/await" advice. async/await improves readability for Promise flows, but it does not solve cancellation, unhandled rejections, callback error paths, stream lifecycle, worker message boundaries, stale responses, or ordering assumptions. Always identify the async abstraction first: callback, Promise, async function, event, timer, fetch/networking, async iterable, Node EventEmitter, Node stream, browser worker, Node worker thread, or child process.

## Apps Script extension standard

Apps Script records in V2 are intentionally small and operational. Every Apps Script record is marked `google_apps_script_extension` and `current_verification_required: true`. For future Apps Script Web App work, first create a file-role map:

- server-side Apps Script `.gs` functions;
- HtmlService browser HTML/JS;
- spreadsheet reads/writes;
- triggers;
- upload/CSV/XLSX processing;
- authorization scopes;
- quotas and deployment behavior needing current Google documentation.

## AI-agent response standard

A safe AI-agent JavaScript review should provide:

- runtime and module-system evidence;
- source-derived language behavior or explicit extension label;
- concrete failure symptom and root-cause pattern;
- related reusable risk IDs;
- specific diagnostics and tests;
- current-verification flags when platform/tooling behavior may have changed.

Generated at: 2026-06-21T05:00:11.155979+00:00
