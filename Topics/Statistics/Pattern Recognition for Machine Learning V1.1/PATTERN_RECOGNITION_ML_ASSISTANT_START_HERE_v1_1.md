# Pattern Recognition and Machine Learning Active Reasoning Pack V1.1

Focused repair pass for the compact active-use pack. This is **not** the full 29-file package.

## Source authority

Primary source: *Fundamentals of Pattern Recognition and Machine Learning*, Second Edition, Ulisses Braga-Neto, 2024.

Authority order used in this pack:

1. Original uploaded book source.
2. Current V1 active pack.
3. V1.1 repair prompt.
4. Current official software documentation only when current behavior is needed.
5. General ML/statistical reasoning.
6. Restaurant/OMAKAI applied overlay as extension only.

## How to use the active pack

Start with `pattern_recognition_ml_assistant_context_v1_1.json`, then open the file that matches the task:

- Algorithm choice: `pattern_recognition_ml_algorithm_registry_v1_1.json`
- Evaluation/leakage/model-selection review: `pattern_recognition_ml_error_estimation_model_selection_v1_1.json`
- Failure-mode audit: `pattern_recognition_ml_misuse_and_failure_modes_v1_1.json`
- Restaurant analytics: `pattern_recognition_ml_restaurant_analytics_overlay_v1_1.json`
- AI-agent review workflow: `pattern_recognition_ml_ai_agent_workflows_v1_1.json`
- Current software/export claims: `pattern_recognition_ml_current_verification_flags_v1_1.json`

## Source boundary rule

Book-supported ML content is separated from operational extensions. Restaurant analytics and OMAKAI-style examples are not direct book claims. Current Python, scikit-learn, Jupyter, NumPy/SciPy, deep-learning, dataset, and export-schema behavior must be verified from current official documentation, runtime output, or current exports before being asserted.

## OMAKAI-safe restaurant analytics decision gate

Before using ML on restaurant data, ask:

1. What decision are we trying to improve?
2. Is this prediction, classification, clustering, anomaly detection, forecasting, reporting, or causal inference?
3. What is the target?
4. What data exists before the decision?
5. What data would be leakage?
6. Is the sample representative?
7. Are locations comparable or should they be modeled separately?
8. What seasonality, holiday, event, promo, menu, weather, or operational confounders exist?
9. What validation design proves this works?
10. What operational action would change if the model is right?
11. What is the simplest useful non-ML baseline?
12. What would make this conclusion unsafe?

## V1.1 validation snapshot

- JSON files parse: pending manifest says true after finalization.
- Expected folder files: 16
- Active records after V1.1: 204
- Restaurant overlay records: 18
- Reusable risk records: 29
- Current verification flags: 16
- Confidence distribution: {'high': 60, 'medium': 62, 'low': 82}

## Known limitations

This pack is designed for reasoning, review, and safe problem framing. It does not include trained models, current API verification, vendor export-schema verification, real OMAKAI data, or causal-inference proof. Use the restaurant overlay as a low-confidence operational extension until validated with real data and current schemas.
