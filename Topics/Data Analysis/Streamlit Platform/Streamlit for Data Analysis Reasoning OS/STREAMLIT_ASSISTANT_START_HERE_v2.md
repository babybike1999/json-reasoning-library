# Streamlit Control-Plane & Data-App Safety Library V2

Generated: 2026-06-21

Use this package as a compact safety and architecture reference for AI agents modifying Streamlit data apps, control panels, file-validation workflows, API-safe interfaces, owner/admin dashboards, and nontechnical-user workflows.

## Authority order
1. Original uploaded *Streamlit for Data Science* source
2. Current generated package as draft input
3. Repair prompt
4. Current official Streamlit documentation where checked
5. General operational reasoning

## Source limitation
The uploaded Early Access source lists chapters 1-13, but accessible chapter content is chapters 1-7 only. Chapters 8-13 remain marked missing. The accessible `ch008.xhtml` file is Chapter 7, **Exploring Streamlit Components**, not book Chapter 8.

## Recommended active-use files
- `streamlit_assistant_context_v2.json` — compact agent context and rules
- `streamlit_control_plane_safety_pack_v2.json` — risk IDs, live-action rules, and review pack
- `streamlit_rerun_state_caching_v2.json` — execution, rerun, state, cache, and side-effect records
- `streamlit_forms_side_effects_workflows_v2.json` — dry-run/live and file workflow state machines
- `streamlit_auth_secrets_permissions_v2.json` — auth, authorization, secrets, redaction, downloads
- `streamlit_testing_observability_v2.json` — tests and review patterns
- `streamlit_app_templates_v2.json` — 10 practical app templates
- `streamlit_current_verification_flags_v2.json` — current-doc/runtime verification flags

## Non-negotiable rules
Do not treat Streamlit as a backend. Do not treat session state as durable storage or authorization. Do not treat hidden pages/widgets as authorization. Do not trigger live writes from top-level rendering. Do not cache secrets or sensitive user-specific data without explicit isolation and risk handling. For API/database/file-changing operations, require preview or dry-run, confirmation, backend authorization, idempotency, result states, and test evidence.
