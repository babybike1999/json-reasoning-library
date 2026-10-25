# SQL Cookbook Reasoning OS — Start here

## Source and purpose

This is a practical SQL reasoning package based only on **SQL Cookbook, Second Edition**, by **Anthony Molinaro and Robert de Graaf**, published by **O’Reilly**. The edition history says December 2020; the copyright notice says 2021. The metadata dates and two visible publication identifiers are preserved separately in `sql_cookbook_source_map_v1.json`.

The package contains **465 distinct reasoning records**, including all **164 recipes across 14 chapters**, plus source-supported concepts from the two appendices. It is not a copied recipe archive, executable code library, current vendor manual, or proof that a business query is correct.

## Load the smallest useful context

Start with `sql_cookbook_assistant_context_v1.json` (159,703 bytes). It contains compact routing cards, the reasoning gate, source-issue warnings, and workflow choices. Load the relevant topical JSON file for the complete records. Use `sql_cookbook_reasoning_os_full_v1.json` when a complete corpus is needed, not by default for every query.

Each topical file has a `records` array and `section_key`. A repeated record ID is the same canonical record, not additional evidence. The file index identifies the modules and counts. Full OS topical arrays intentionally repeat canonical records for direct use.

## Authority order

1. Current schema, table definitions, columns, keys, and constraints.
2. Current result samples and expected output.
3. Actual database dialect and version.
4. Current errors, plans, logs, and runtime evidence.
5. Current metric definitions, SOPs, accounting rules, and reporting requirements.
6. Current official database documentation.
7. Source-supported SQL Cookbook concepts.
8. Cross-recipe source synthesis.
9. Marked analytics and restaurant applications.
10. Marked AI-agent workflows.
11. General advice.

The book must not override the actual schema, observed data, dialect, or approved metric definitions.

## SQL reasoning gate

1. What exact business or data question is being answered?
2. What does one output row represent?
3. Which verified tables or input rowsets are involved?
4. What does one row in each input represent?
5. Which complete keys define the relationships?
6. Are the relevant keys unique on the sides assumed unique?
7. What database product and exact version will execute the query?
8. Which filters define the eligible population?
9. Which boundaries, calendar, and timestamp rules define the reporting period?
10. Which NULL comparisons, counts, replacements, and sorting choices matter?
11. Which reductions, partitions, orders, and frames are required?
12. Could any stage multiply or drop rows unexpectedly?
13. Which output columns, types, categories, and aggregation levels must be delivered?
14. Which concrete fixtures and expected results establish the intended behavior?
15. Which current schema or official documentation claims remain unverified?

## Interpretation and provenance

Every substantive record has a `source_traceability` object and a `derivation` object. The source locator uses `archive-member.html#anchor`, not a fabricated printed page. The source map provides Problem, Solution, and Discussion anchors when present. Recipe 10.2 has a nested Discussion; 14.2 has explanation within Solution and no separate Discussion heading.

Direct source patterns use high confidence in their source grounding, not a promise of runtime correctness. Source synthesis uses medium confidence. Business, restaurant, workflow, and current-verification extensions use low confidence and require live evidence. Suggested tests and input/output-grain annotations are explicitly identified as package-authored validation guidance.

The source-era database baselines are DB2 11.5, Oracle 19c, PostgreSQL 12, SQL Server 2017, and MySQL 8.0. They are historical metadata, not recommendations or current compatibility claims.

## Stop before copying a flagged listing

The source map contains documented source issues. Particularly important are measure-level DISTINCT after joins (3.9–3.10), inconsistent row-to-string syntax (6.10), token-position assumptions (6.14), the MySQL median selection (7.10), the MAD centering expression (7.16), missing-category counts in Benford analysis (7.17), and an unresolved recursive name in Appendix B. A source inconsistency is kept visible rather than silently repaired.

The validation manifest contains six small synthetic counterexamples. These were evaluated with Python or static identifier comparison. **They are not vendor SQL executions**, do not establish current syntax, and do not certify a repaired query. Obtain current official documentation and run a controlled fixture on the actual target database before using a flagged implementation.

## Non-negotiable query safeguards

Identify input/output grain and complete keys before joining. Check match multiplicity before summing. Do not use DISTINCT to hide an unexplained relationship. Distinguish COUNT(*) from COUNT(column), missing values from zero, and window partitions from frames. Define a tie policy wherever ordering affects selected rows or running values. Keep business-day, fiscal-week, and interval endpoints explicit. Retain aggregation-level markers when detail and subtotals share a report.

Generated statement text is not execution authorization. This package authorizes no data changes. A proposed write needs an exact affected-row preview, approved scope, target-specific review, and appropriate recovery controls.

## Applied layers are not book claims

Business and restaurant overlays specify possible supplied inputs and unresolved definition requirements. They do not invent a live Restaurant365, SevenRooms, Uber Eats, or company schema. They provide no organization-specific formulas, causal estimates, staffing conclusions, or integration guarantees. External modules named in the cross-domain file were not uploaded or read.

## Suggested answer contract for an assistant

Present the exact question and result grain; the known schema/dialect evidence; the selected recipe IDs and derivation boundary; the proposed query or unresolved design; the key/NULL/date/aggregation checks; and what was actually tested. State remaining unknowns. A query that parses or executes is not automatically the intended answer, and a readable query is not automatically fast.

## Integrity and limitations

Consult `sql_cookbook_validation_manifest_v1.json` for structural tests, source issues, synthetic checks, counts, and limitations. The checksum file covers the other 28 finalized payload files and deliberately excludes itself. The ZIP contains only the 29 requested deliverables, not the source book, extracted text, font files, or working scripts.

A focused **source-listing repair and target-database test pass** is recommended before executable use, especially for statistics, string aggregation/token ordinals, recursive syntax, and conditional writes. The source-grounded reasoning package remains usable without treating those listings as correct code.
