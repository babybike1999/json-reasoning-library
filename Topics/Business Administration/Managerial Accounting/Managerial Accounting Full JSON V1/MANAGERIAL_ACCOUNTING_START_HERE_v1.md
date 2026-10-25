# Managerial Accounting Reasoning Library · v1

A source-grounded, reusable decision-review library for accounting explanation, FP&A, costing, budgeting, variance investigation and bounded financial recommendations.

## Start here

Load `managerial_accounting_assistant_context_v1.json` with the canonical `hilton_platt_managerial_accounting_reasoning_v1.json`. Consult the source map for provenance and coverage, and the model tests for synthetic calculations. The context is a guide, not a replacement for the substantive records.

For practical retrieval, search a management question rather than only an accounting term. Six route records begin with questions such as “Sales fell, but labor percentage rose” and “This product looks unprofitable after overhead allocation.” Routes lead to models, required evidence and selective risks.

The working sequence is: **define the decision → establish the reporting boundary → inspect the data → select the model → state assumptions → calculate → reconcile → investigate explanations → evaluate consequences → recommend a bounded next step.**

## Verified source identity

**Ronald W. Hilton and David E. Platt, _Managerial Accounting: Creating Value in a Dynamic Business Environment_, Thirteenth Edition.** The title and copyright pages establish the edition, authors, McGraw Hill LLC publisher, printed ISBN **978-1-265-04679-8**, and MHID **1-265-04679-4**.

The copyright page says **©2023**. Embedded EPUB metadata records **2022-07-06**, modified at 2022-07-06T09:22:07Z. Both are preserved; an independently verified commercial publication day is **not established**. The OPF’s seven-digit identifier7130806 is retained as opaque, not substituted for the printed ISBN. Raw publisher and creator metadata variants are retained in the source map.

The uploaded file is a ZIP containing an unpacked EPUB3 tree. Locators use actual `OEBPS/*.xhtml` filenames, actual anchors when available, and defined extraction block ranges. Printed page labels are separate; there are no invented PDF page numbers.

## What is included

**157 canonical records and 157 claim-ledger entries:**65 concepts,54 model specifications,4 decision records,16 diagnostic risks,5 workflows,7 application extensions and 6 question routes. Each model includes input/output definitions, units, periods, domains, assumptions, formulas, signs, rounding, reconciliation, edge cases and test links.

There are **193 source locators**, **54 inspectable Python implementations**, **89 numerical/input-guard tests**, and **8 separately labeled reasoning cases**. All figures in the test suite are original synthetic data, except the synthetic cost bridge explicitly supplied in the brief. No textbook exercise solution or real company outcome is represented.

Evidence layers are explicit: textbook explanation, analytical derivation, application extension, project evidence and current external verification. No real project data or independently verified current external material is included. Diagnostic prompts and practical workflows are authored safeguards, not automatically statements by the authors.

## Actual source coverage

Selected substantive passages were read and extracted from **all 17 chapters and all 3 supplementary appendices**. This is **not exhaustive textbook coverage**. Reading a contents entry does not count as reading or extracting its subject. Source-span counts are navigation measures, not percentages of the textbook verified.

| Chapter | Actual body title | Linked records* |
|---|---|---:|
| 1 | The Crucial Role of Managerial Accounting in a Dynamic Business Environment | 6 |
| 2 | Basic Cost Management Concepts | 9 |
| 3 | Product Costing and Cost Accumulation in a Batch Production Environment | 5 |
| 4 | Process Costing and Hybrid Product-Costing Systems | 3 |
| 5 | Activity-Based Costing and Management | 7 |
| 6 | Activity Analysis, Cost Behavior, and Cost Estimation | 7 |
| 7 | Cost-Volume-Profit Analysis | 6 |
| 8 | Variable Costing and the Measurement of ESG and Quality Costs | 6 |
| 9 | Financial Planning and Analysis: The Master Budget | 6 |
| 10 | Standard Costing and Analysis of Direct Costs | 6 |
| 11 | Flexible Budgeting and Analysis of Overhead Costs | 6 |
| 12 | Responsibility Accounting and the Balanced Scorecard | 5 |
| 13 | Investment Centers and Transfer Pricing | 5 |
| 14 | Decision Making: Relevant Costs and Benefits | 12 |
| 15 | Target Costing and Cost Analysis for Pricing Decisions | 7 |
| 16 | Capital Expenditure Decisions | 13 |
| 17 | Allocation of Support Activity Costs and Joint Costs | 8 |

*Some records can link more than one chapter; row totals are not the canonical unique-record count. Practical extension records need not have a chapter number.

The supplementary appendices cover internal controls/Sarbanes–Oxley, compound interest/present value, and inventory management. Their reading is also selective. Legal rules are historical source material, not current verified applicability.

The source map inventories36 XHTML files, including814 heading elements,577 XHTML table elements,651 figure elements,1,341 image references,225 explicitly labeled exercises,259 problems and 39 cases. These are **XML/pedagogical-label inventories**, not claims that all these objects were substantively read. Figure/table/image counts overlap and must not be added as unique exhibits. Unlabeled examples and image-contained sub-tables are not independently enumerated. Only44 selected embedded formula images were visually inspected. No OCR was used.

All17 chapter checkpoints and 3 supplementary checkpoints were actually saved during construction. The final package has one canonical record set; working snapshots are not bundled as duplicate libraries. The original textbook and full extracted source text are excluded.

## Preserved distinctions and unresolved source questions

The process-costing implementation is **weighted average**, not an invented FIFO calculation. The edition mentions FIFO but does not develop it into the detailed procedure used here. Later-department transferred-in calculations, a general LP solver, multiple regression, learning-curve calculations and real-option pricing are not implemented. Advanced material mix/yield variance decompositions were not filled in as textbook claims.

Purchase-price and usage-price variances remain separate. Fixed-overhead volume variance is retained as an allocation reconciliation with source-appropriate sign caution, not proof of inefficient operations. Direct, step-down and reciprocal support allocation are separate functions; the step-down sequence is explicit. Initial-investment and average-investment ARR are different methods.

The **chapter 15 General Formula image** appears to repeat a total-variable-cost markup formula. The library preserves this question and labels its generalized excluded-cost markup equation as an analytical derivation, not a literal transcription or silent source correction. The capacity-cost opportunity proxy and the authors’ DCF reinvestment/ranking framing are also qualified rather than silently replaced or generalized. See `source_caveats` for exact locators.

## Validation and rerunning

The delivered report records the actual final execution. Structural and numerical success does not establish independent source interpretation, current legal/tax authority or suitability for a real project. Overall status remains **requires_human_review**, not universal approval. Current external verification is **blocked** because web access was unavailable. The8 reasoning cases require human interpretation review and are not included in automatic numerical pass counts.

The source locator audit checks the original ZIP hash, actual internal files/anchors, selected text-span hashes and reviewed image assets. It does not certify every paraphrase or every unreviewed page. An initial whitespace/empty-element normalization mismatch in the source-recheck code was diagnosed and corrected; source bytes were not altered to make it pass.

Run with Python3.10+ from the unpacked directory:

```bash
python managerial_accounting_validate_v1.py --check-checksums
```

Without the original ZIP, source-byte revalidation is reported **blocked**, while structural and synthetic numerical checks still run. To recheck the exact uploaded source:

```bash
python managerial_accounting_validate_v1.py \
  --source-zip "/path/to/Managerial Accounting.epub.zip" \
  --check-checksums
```

Default output goes to the console and does not mutate packaged files. Save a **new** report with `--report /path/to/new_report.json`. Overwriting the packaged report invalidates its old checksum; regenerate the manifest only after all changes are final. The packaged report itself predates checksum generation, so its checksum section is correctly `not_run`; the finalized manifest and reopened ZIP were checked separately during packaging.

The validator rejects duplicate JSON keys, nonfinite constants, duplicate IDs, invalid types/statuses and unresolved references. It executes only allowlisted explicit functions, never formula strings. Missing/null/malformed inputs and invalid domains are tested.89 executed tests passed, with zero numerical failures at final validation; inspect the actual report rather than treating this sentence as the source of test evidence.

## Application limits

The seven small extensions address monthly P&L commentary, labor capacity, location/channel profitability, food purchasing/yield, warehouse/central preparation, software/equipment/process investment, and cash/working capital. They are not claims about a particular company.

Before use, supply the real chart of accounts, sales and margin definitions, units, fiscal periods, opening balances, allocation rules, capacity constraints, standards, hurdle rates and approved policies. For hospitality, distinguish taxes, tips, discounts, refunds, delivery charges and commissions; distinguish purchase, usable and portion units; and distinguish paid, scheduled, worked and productive hours. Never turn an unexplained inventory residual into proven waste or a favorable price variance into an overall performance verdict.

NPV supports dated **annual anniversaries**, not an unspecified day-count convention. IRR supports conventional cash flows with a valid supplied bracket. Tax cash models use supplied hypothetical rates and eligibility assumptions, not a current tax engine. Cash commitments, financing conventions, terminal effects and operational constraints require independent review.

No company workbook was recalculated, no SQL query or BI dashboard was executed, no software integration was tested, and no professional accounting/tax/legal assurance is provided. Local synthetic Python functions were actually run. A numerical result is a conditional calculation, not a mandate to close a location, change staffing, borrow money or accept a contract.

## File guide

| File | Purpose |
|---|---|
| `hilton_platt_managerial_accounting_reasoning_v1.json` | Canonical substantive records and claim ledger |
| `managerial_accounting_source_map_v1.json` | Bibliography, EPUB locators, coverage, inventories and caveats |
| `managerial_accounting_model_tests_v1.json` | Independent synthetic expectations and reasoning cases |
| `managerial_accounting_assistant_context_v1.json` | Compact active-use instructions and question routes |
| `MANAGERIAL_ACCOUNTING_START_HERE_v1.md` | This guide |
| `managerial_accounting_validate_v1.py` | Validator and explicit model implementations |
| `managerial_accounting_validation_report_v1.json` | Executed results and unresolved review boundaries |
| `managerial_accounting_file_index_v1.json` | File dependencies and namespace conventions |
| `managerial_accounting_checksums_v1.sha256.json` | SHA256 values for the other eight finalized files |

The ZIP contains these nine files only. The checksum manifest excludes itself; the ZIP lives outside the package directory and was reopened to verify all member bytes.

**A financial model is useful only when its accounting definitions, mathematical logic, assumptions and decision context fit together.**
