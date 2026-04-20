---
module: 8
section: "8.4"
title: "Point Estimation"
---

A point estimate is a single number computed from a sample used as the best guess for an unknown population parameter.

**Common point estimators**
- **Sample mean** x̄ = (1/n) Σ xᵢ — estimates the population mean μ.
- **Sample proportion** p̂ = x/n — estimates the population proportion P. Used in classification and A/B testing.
- **Sample variance** s² = (1/(n − 1)) Σ (xᵢ − x̄)² — estimates the population variance σ². The n − 1 (Bessel's correction) makes s² unbiased.

**Desirable properties of good estimators**
1. **Unbiasedness** — on average across samples, the estimator equals the true parameter. E.g., x̄ is unbiased for μ.
2. **Consistency** — the estimator converges to the true value as n grows. Most standard estimators are consistent under random sampling.
3. **Efficiency** — among unbiased estimators, the one with the smallest variance. Efficient estimators give more stable predictions.

In AI we want models whose learned parameters are unbiased, consistent, and efficient — ensuring reliable learning that improves with more data and doesn't fluctuate wildly sample to sample.
