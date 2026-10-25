# Data Structures and Algorithms with JavaScript — Assistant Start Here

## Purpose

This package is a source-traceable reasoning system built from Michael McMillan’s *Data Structures and Algorithms with JavaScript*. It is designed to help future AI assistants select data structures and algorithms for JavaScript work, especially Google Apps Script, Google Sheets automations, report processors, uploads, forms, scorecards, dashboards, and internal tools.

It is not a book summary, an exercise-solution manual, a code-copy archive, or a generic glossary. The package contains **463 reasoning records** plus a complete source map. The compact assistant context is **191,687 bytes**, within the required 75–200 KiB range.

## Source identity and caution

The uploaded EPUB contains a material metadata inconsistency:

- EPUB metadata and the copyright page: **Data Structures and Algorithms with JavaScript**
- Title page: **Data Structures and Algorithms in Javascript** and **Second Edition**
- Copyright page: March 2014 **First Edition**, with a **Second Release** dated October 21, 2015

The package preserves that mismatch. The source uses a SpiderMonkey-based JavaScript shell and says Node.js may require translations. Its October 20, 2015 update note reports clarity fixes, a Mergesort change, repository reorganization, and parallel Node-compatible code. Algorithmic reasoning transfers more reliably than literal source-era implementations.

**Google Apps Script is not SpiderMonkey, Node.js, or browser JavaScript.** Current V8 support, services, quotas, triggers, authorization, deployment, Web Apps, Spreadsheet behavior, Map/Set/sort behavior, persistence, locks, file uploads, repositories, and errata must be verified from current authoritative sources and current project evidence.

## Authority order

Use evidence in this order:

1. Current project code and runtime behavior
2. Current error logs, execution logs, stack traces, and user reports
3. Current data shape in Sheets, CSV, XLSX, APIs, or uploaded files
4. Current Google Apps Script documentation and quotas
5. Current JavaScript runtime documentation when relevant
6. Current business requirements, SOPs, and workflow rules
7. Source-supported data-structure and algorithm concepts from the book
8. Cross-chapter synthesis from the source
9. Google Apps Script translation-layer extensions
10. Internal-tool workflow extensions
11. AI-agent workflow extensions
12. General programming advice

## Data-structure selection gate

Before proposing code, answer:

1. What problem is the script solving?
2. What is the input data shape?
3. What is the output data shape?
4. What uniquely identifies each record?
5. Do we need order, uniqueness, lookup, grouping, hierarchy, dependency, or processing order?
6. What data structure fits that need?
7. What operation dominates runtime?
8. What is the expected row count or scale?
9. Are we repeatedly scanning data that could be indexed?
10. Are we calling Apps Script services inside loops?
11. What validation must happen before transformation?
12. What happens on duplicate, missing, malformed, or unmapped data?
13. Can errors be collected without writing live output?
14. What current Apps Script behavior must be verified?
15. What test proves the structure and algorithm work?

## Operational defaults

- Use arrays for ordered tabular transport and rectangular batch boundaries; convert rows to named records when business logic becomes nontrivial.
- Build a validated header map once. Never rely on hard-coded positions across report versions.
- Replace repeated key scans with one lookup index when query frequency and key cardinality justify it.
- Use sets for uniqueness and expected-versus-actual coverage, but keep occurrence lists/maps when counts, order, or duplicate evidence matter.
- Use queues for staged processing only with stable item IDs, durable state, bounded retry, idempotency, concurrency control, and structured results.
- Use binary search only on data proven sorted by the same comparator. For repeated exact-key search, a validated lookup map is often clearer.
- Prefer a verified current built-in sort to a hand implementation unless a custom algorithm is specifically justified.
- Use trees and graphs only when real hierarchy, path, reachability, cycle, or dependency questions require them.
- Use greedy or dynamic-programming techniques only after objective, constraints, state, scale, correctness, and reconstruction requirements are explicit.
- Read Sheets in bounded batches, transform in memory, validate the full proposed result, preview, then batch-write. Current service behavior still requires verification.
- Preserve original row/sheet provenance through every filter, sort, group, join, and error.
- Make every live side effect idempotent or recoverable; report mixed outcomes per item rather than only returning a Boolean or one exception.

## Package routing

Load **`data_structures_algorithms_js_assistant_context_v1.json`** first for compact routing. Then open only the focused file needed:

- `data_structures_algorithms_js_source_map_v1.json` — exact source identity, structure, anchors, counts, figures/tables, updates, and limitations
- `data_structures_algorithms_js_core_concepts_v1.json` — thesis, terminology, data-structure and algorithm overview
- topic files — arrays; lists/linked lists; stacks/queues; dictionaries/hashing; sets; trees; graphs; sorting; searching; dynamic programming/greedy; complexity
- `data_structures_algorithms_js_google_apps_script_translation_layer_v1.json` — guarded Apps Script transfer rules
- `data_structures_algorithms_js_internal_tool_patterns_v1.json` — R365, Uber Eats, SevenRooms, uploads, forms, scorecards, dashboards, routing, audit, retry patterns
- `data_structures_algorithms_js_spreadsheet_data_workflows_v1.json` — parse/header/record/join/group/validate/preview/write/recovery patterns
- `data_structures_algorithms_js_failure_modes_and_pitfalls_v1.json` — required risk registry
- `data_structures_algorithms_js_decision_rules_v1.json` — structure and algorithm choice rules
- `data_structures_algorithms_js_diagnostic_questions_v1.json` — concrete evidence-gathering questions
- `data_structures_algorithms_js_ai_agent_workflows_v1.json` — 18 review/design workflows
- `data_structures_algorithms_js_current_verification_flags_v1.json` — all time-sensitive runtime/platform boundaries
- `data_structures_algorithms_js_cross_domain_connections_v1.json` — routing to separate language, architecture, data, HCD, operations, and restaurant modules
- `data_structures_algorithms_js_reasoning_os_full_v1.json` — load only when full package-wide reasoning is required

## High-priority risk IDs

The failure file includes every required risk, including:

`dsa-risk-array-only-thinking`, `dsa-risk-wrong-data-structure`, `dsa-risk-nested-loop-timeout`, `dsa-risk-repeated-sheet-service-call`, `dsa-risk-missing-lookup-map`, `dsa-risk-duplicate-not-detected`, `dsa-risk-header-index-drift`, `dsa-risk-row-shape-assumption`, `dsa-risk-mutation-during-iteration`, `dsa-risk-unstable-sort-assumption`, `dsa-risk-binary-search-unsorted-data`, `dsa-risk-set-versus-list-confusion`, `dsa-risk-queue-retry-duplication`, `dsa-risk-stack-queue-order-confusion`, `dsa-risk-tree-overengineering`, `dsa-risk-graph-overengineering`, `dsa-risk-greedy-local-optimum`, `dsa-risk-dp-overengineering`, `dsa-risk-source-era-js-runtime-assumption`, `dsa-risk-node-spidermonkey-appsscript-confusion`, `dsa-risk-native-map-set-verification`, `dsa-risk-quota-timeout`, `dsa-risk-live-write-before-validation`, `dsa-risk-partial-failure-unstructured`, and `dsa-risk-idempotency-missing`.

## Record distribution

- **core_thesis**: 1
- **core_principles**: 12
- **terminology_registry**: 38
- **data_structure_records**: 12
- **algorithm_records**: 16
- **array_records**: 21
- **list_records**: 22
- **stack_queue_records**: 15
- **dictionary_hash_records**: 17
- **set_records**: 12
- **tree_records**: 18
- **graph_records**: 18
- **sorting_records**: 19
- **searching_records**: 14
- **dynamic_programming_and_greedy_records**: 16
- **complexity_and_performance_records**: 12
- **google_apps_script_translation_records**: 20
- **internal_tool_pattern_records**: 21
- **spreadsheet_data_workflow_records**: 20
- **failure_modes_and_pitfalls**: 25
- **decision_rules**: 22
- **diagnostic_questions**: 37
- **ai_agent_workflows**: 18
- **current_verification_flags**: 17
- **cross_domain_connections**: 20

## Non-negotiable source boundary

Do not claim the book discusses Google Apps Script, R365, SevenRooms, Uber Eats, restaurant operations, warehouse workflows, forms, scorecards, dashboards, retries, idempotency, concurrency, or current native Map/Set behavior unless a record explicitly labels the claim as an extension. Source-direct claims, source synthesis, Apps Script translation, spreadsheet workflow, internal-tool application, AI workflow, and current-verification flags must remain distinct.
