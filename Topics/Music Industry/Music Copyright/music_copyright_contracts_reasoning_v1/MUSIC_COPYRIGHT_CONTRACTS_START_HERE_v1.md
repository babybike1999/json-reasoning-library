# Music Copyright Contracts Reasoning Library — Start Here

## What this library is for

Use it to map music rights, review proposed clauses, identify missing documents and facts, prepare negotiation questions, and organize an attorney handoff. It supports issue spotting and contract comprehension. It does not issue an automatic legal opinion, provide ready-to-sign language, or clear a release.

No agreement facts, collaborator contributions, ownership shares, fees, royalty points, deadlines, or approvals were supplied. Keep them open until evidence and commercial instructions are provided.

## Source and currentness

The source is *Music Copyright Law* by David J. Moser and Cheryl L. Slay, Course Technology PTR/Cengage, copyright 2012. The authors say the edition’s legal discussion was current as of mid-2011. The numbered book pages 1–304 map to PDF pages 19–322 (one-based PDF page = printed Arabic page + 18). A usable embedded, apparently OCR-derived text layer was extracted; no OCR service was used. Selected high-consequence passages were checked against page images. See the scan audit for exact coverage, blank pages, quality limits, metadata, and hashes.

A small set of propositions was separately checked against current U.S. Title 17 and U.S. Copyright Office material, accessed 2026-09-28. That does not make the whole library current. Case-specific joint-owner, sampling, state contract, foreign, platform, rate, deadline, and project questions remain open; see `verification_tasks`.

## Recommended use

1. Read `music_copyright_contracts_context_v1.md` as the compact entry point.
2. Load records from `music_copyright_contracts_reasoning_v1.json` that match the actual asset and decision.
3. Follow `mcl-workflow-contract-review` and `mcl-workflow-chain-of-title` in order.
4. Keep composition, master, version, permission, ownership, administration, collection, royalty, service payment, credit, and file delivery separate.
5. Link each claim to a source locator or current authority. Mark unsupported facts unresolved and ask a question tied to a specific action.
6. Run the synthetic cases as review scenarios; they are not real disputes or precedents.

## Library inventory

The canonical JSON contains 12 concepts, 9 legal review gates, 13 contract-review records, 9 applied workflows, 13 reusable risks, 12 diagnostic questions, 4 review workflows, 8 synthetic cases, 9 verification tasks, 20 source locators, and 12 authority references. Counts are generated from the delivered JSON.

The requested Music Publishing JSON was not supplied, so no cross-library records are linked. The package excludes the source book and the full extracted text.

## Files

- `music_copyright_contracts_reasoning_v1.json` — canonical record library.
- `music_copyright_contracts_context_v1.md` — compact assistant entry point.
- `music_copyright_source_and_scan_audit_v1.json` — verified metadata, extraction, page mapping, chapter coverage, gaps, and source-quality audit.
- `music_copyright_validation_report_v1.json` — mechanical, source, currentness, semantic, and package validation outcomes.
- `music_copyright_checksums_v1.sha256.json` — SHA-256 for the five payload files other than this checksum file; the outer ZIP is not included to avoid a self-referential archive hash.
- `music_copyright_contracts_reasoning_v1.zip` — package containing the six files above.

This library makes a next question more precise. It does not make uncertain legal answers sound certain.
