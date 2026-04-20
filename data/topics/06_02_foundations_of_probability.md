---
module: 6
section: "6.2"
title: "Foundations of Probability"
---

Probability is the mathematical language of uncertainty. A random experiment has a sample space Ω containing all possible outcomes, and an event is any subset of Ω.

**Types of events**
- Simple event: exactly one outcome (e.g., rolling a 3 → {3}).
- Compound event: multiple outcomes (e.g., rolling even → {2,4,6}).
- Certain event: P = 1 (entire sample space).
- Impossible event: P = 0 (empty set).

**Axioms of probability**
1. Non-negativity: P(A) ≥ 0.
2. Normalization: P(Ω) = 1.
3. Additivity: if A and B are mutually exclusive, P(A ∪ B) = P(A) + P(B).

**Classical vs. empirical probability**
- Classical: P(A) = favorable outcomes / total outcomes (requires equally likely outcomes). Example: rolling an even number on a fair die → 3/6 = 0.5.
- Empirical: P(A) = times A occurred / total trials. Example: 58 heads in 100 flips → 0.58.

**Set operations**
- Complement: P(Aᶜ) = 1 − P(A).
- Union: P(A ∪ B) = P(A) + P(B) − P(A ∩ B) (general rule; if mutually exclusive, the overlap term is 0).
- Intersection A ∩ B: outcomes in both events — the basis of joint probabilities.

These foundations power AI systems that reason under uncertainty, from spam filters to medical diagnosis.
