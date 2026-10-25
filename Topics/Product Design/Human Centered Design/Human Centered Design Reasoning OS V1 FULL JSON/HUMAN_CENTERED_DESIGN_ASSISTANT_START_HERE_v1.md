# Human-Centered Design, Usability, and Error-Prevention Reasoning OS V1

This V1 package is a semantic-compression repair of the previous package. It keeps source inventory, edition metadata, terminology distinctions, source map, reusable risk IDs, and operational-software usefulness, while removing the universal HCD boilerplate pattern.

## Source

- Title: The Design of Everyday Things: Revised and Expanded Edition
- Author: Don Norman
- Edition: Revised and expanded edition
- Publisher/year: Basic Books, a member of the Perseus Books Group, 2013
- Source format: Uploaded ZIP containing an EPUB 2 package with OPF, NCX, XHTML/HTML, CSS, and JPEG figures.
- Original/revised title note: originally *The Psychology of Everyday Things*; later retitled *The Design of Everyday Things*.

## Use this package

1. Start with `human_centered_design_assistant_context_v1.json` for repeated assistant use.
2. Use `hcd_terminology_and_distinctions_v1.json` when terminology matters.
3. Use `hcd_human_error_diagnostic_pack_v1.json` for slip/mistake and error diagnostics.
4. Use `hcd_discoverability_mapping_feedback_constraints_v1.json` for action, mapping, feedback, and constraint review.
5. Use `hcd_knowledge_and_conceptual_models_v1.json` for memory burden, system image, and gulf analysis.
6. Use `hcd_design_diagnostic_questions_v1.json` to drive reviews from evidence instead of opinion.
7. Use `hcd_current_verification_flags_v1.json` before making current accessibility/platform/browser/framework claims.

## Canonical review gate

1. Who is the user?
2. What goal are they trying to accomplish?
3. What actions can they perceive?
4. What signifiers indicate where or how to act?
5. What does the user believe will happen?
6. How well does action map to effect?
7. What must the user remember?
8. What knowledge exists in the world?
9. What system state is visible?
10. What feedback follows the action?
11. What invalid or dangerous actions are allowed?
12. Is the observed failure a slip or a mistake?
13. What can the design prevent?
14. What happens after error?
15. Can the user recover without expert help?
16. What observed user evidence supports the diagnosis?

Individual records reference this gate when broad review is needed. They do not reproduce the full gate.

## V1 repair principles

- Each record names its primary mechanism.
- Family-specific schemas replace the old universal record template.
- Human-error records distinguish slips, mistakes, capture slips, description-similarity slips, mode errors, memory lapses, rule-based mistakes, and knowledge-based mistakes.
- Feedback, mapping, and constraints are not interchangeable.
- Operational, form, status-state, and AI-agent records are labeled as applied extensions, not direct source claims.
- Current platform/accessibility claims require current verification.
