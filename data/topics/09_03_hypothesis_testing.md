---
module: 9
section: "9.3"
title: "Hypothesis Testing"
---

Hypothesis testing is a formal method for deciding, using sample data, whether evidence supports rejecting a default claim.

**The two hypotheses**
- Null hypothesis H₀: default position — no effect, no difference, no change.
- Alternative H₁: the claim we're seeking evidence for.

You never "prove" H₁; you either reject H₀ in its favor or fail to reject H₀.

**Test statistic**
Test stat = (sample statistic − null value) / standard error. It measures how many standard errors the observation is from what H₀ predicts.
- Use z when σ is known or n is large.
- Use t when σ is unknown and n is small.

**p-value**
Probability of observing data as extreme as ours if H₀ were true. Small p-values are evidence against H₀.
- p < α → reject H₀ (statistically significant).
- p ≥ α → fail to reject H₀.

**Significance level α** (usually 0.05) is the acceptable false-positive rate.

**Six-step procedure**
1. State H₀ and H₁.
2. Choose α (0.05 or 0.01).
3. Compute test statistic.
4. Compute p-value.
5. Decide: reject or fail to reject H₀.
6. Interpret in context.

**Example — model comparison**
Current model: 150/200 correct (75%). New model: 160/200 (80%). Two-proportion z-test gives z ≈ 1.69, p ≈ 0.045. Since p < 0.05, reject H₀ — new model is significantly better at α = 0.05.

**Uses in AI**: A/B testing, model comparison, feature-impact analysis.
