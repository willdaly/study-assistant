---
module: 6
section: "6.4"
title: "Bayes' Theorem"
---

Bayes' Theorem reverses conditional probabilities — it lets us compute the probability of a cause given an observed effect.

**Formula**
P(A | B) = P(B | A) · P(A) / P(B)

- P(A) — prior: belief about A before seeing evidence.
- P(B | A) — likelihood: probability of observing B if A is true.
- P(B) — marginal likelihood / total probability of the evidence.
- P(A | B) — posterior: updated belief after seeing B.

**Worked example — medical testing**
- Disease prevalence P(D) = 0.01.
- Sensitivity P(T | D) = 0.90; false-positive rate P(T | Dᶜ) = 0.05.
- Marginal: P(T) = 0.9·0.01 + 0.05·0.99 = 0.0585.
- Posterior: P(D | T) = (0.9 · 0.01) / 0.0585 ≈ 0.154.

So even with a seemingly accurate test, a positive result only means ~15% chance of disease when the disease is rare. This is the base-rate effect.

**Weather example**
P(rain) = 0.3, P(wet grass | rain) = 0.9, P(wet grass) = 0.4 → P(rain | wet grass) = 0.9·0.3/0.4 = 0.675.

**Why it matters in AI**
- Spam filtering (Naive Bayes classifier).
- Bayesian networks for reasoning under uncertainty.
- Iterative belief-updating as new evidence arrives (foundation of online learning and many recommenders).
