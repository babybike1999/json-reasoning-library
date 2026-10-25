# Statistical Inference Reasoning OS V2 — Start Here

**Repair type:** focused V2 repair, not a full rebuild.  
**Source authority:** *Statistical Inference*, Second Edition, George Casella and Roger L. Berger.  
**Source file:** `Statistical Inference (Chapman & Hall_CRC Texts in -- George Casella, Roger L_ Berger -- Texts in Statistical Science, 2ed, 2024.pdf`.  
**Source SHA-256:** `bd85bdce3cfd071ceb16456247b701d827269e0b0b702372dcf068bdcefa18bc`.

## Authority order

1. Original uploaded book source.
2. Current generated Statistical Inference Reasoning OS package as draft.
3. V2 repair prompt.
4. General statistical reasoning.

The original book is authoritative for source-derived mathematical claims. V2 applied workflows, AI-agent routines, code-review guidance, and current software-verification flags are extensions. Do not present them as author claims.

## How to use the OS

Start with the compact context file, then move to the theorem, assumption, risk, and diagnostic registries. For a statistical task, identify whether the user needs an estimator, a test, an interval, a model check, prediction, simulation, or software review. State the sample space, support, parameter space, and assumptions before recommending a method.

## Core checks before any inference

- What is random, what is observed, and what is the target parameter or estimand?
- What is the sample space/support and is it discrete, continuous, or mixed?
- Are observations iid? If not, which theorem or method still applies?
- Which distribution family and parameterization are being used?
- Which assumptions authorize the estimator, test, interval, or approximation?
- What does the selected result not guarantee?

## Interpretation guardrails

A likelihood is not a probability distribution over parameters unless a Bayesian prior/posterior model is specified. A p-value is not the probability that the null hypothesis is true. A frequentist confidence interval has repeated-sampling coverage; it is not automatically a Bayesian posterior probability statement. Asymptotic methods are approximations, not finite-sample guarantees.

## Regression and ANOVA guardrails

For ANOVA, simple linear regression, logistic regression, robust regression, and errors-in-variables models, state the model and distribution/design assumptions. Check independence, variance structure, linear mean or link form, leverage/outlier behavior, and the exact target of prediction or interval estimation.

## Current-verification warning

The textbook supports mathematical reasoning. Current software defaults, Python/R/Excel functions, package APIs, RNG behavior, bootstrap implementations, optimization behavior, and regression diagnostics must be verified from current documentation, current code, and simulations where appropriate.

## Recommended active-use files

- `STATISTICAL_INFERENCE_ASSISTANT_START_HERE_v2.md`
- `statistical_inference_assistant_context_v2.json`
- `statistical_inference_theorem_registry_v2.json`
- `statistical_inference_assumption_registry_v2.json`
- `statistical_inference_misuse_and_failure_modes_v2.json`
- `statistical_inference_diagnostic_questions_v2.json`
- `statistical_inference_decision_rules_v2.json`
- `statistical_inference_current_verification_flags_v2.json`
