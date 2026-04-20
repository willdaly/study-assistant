---
module: 8
section: "8.5"
title: "Bias and Variability"
---

**Bias**
Systematic error that causes an estimator to consistently miss the true value in one direction. A biased thermometer that always reads 1°C high is accurate-looking but off. The sample mean x̄ is unbiased for the population mean μ. In AI, biased models can systematically favor or disadvantage a group.

**Variability (variance)**
How much the estimator changes from sample to sample. Low variability = consistent results; high variability = wildly varying estimates. Complex models that are overly sensitive to the training data typically have high variance — this shows up as overfitting.

**The bias–variance trade-off**
- Simple model → high bias, low variance → underfitting.
- Complex model → low bias, high variance → overfitting.
- Goal: balance both to generalize well.

Practical levers:
- More data reduces variance.
- Regularization (Ridge, Lasso) intentionally adds a bit of bias to cut variance.
- Cross-validation estimates generalization and helps pick the right complexity.

**Dartboard analogy**
- High bias / low variance: tight cluster far from bullseye.
- Low bias / high variance: scattered around the bullseye on average.
- High bias / high variance: scattered and off-center (worst).
- Low bias / low variance: tightly clustered at the bullseye (the goal).

Understanding this trade-off is why some models generalize while others fail in production.
