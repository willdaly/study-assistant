---
module: 7
section: "7.4"
title: "Expectation and Variance"
---

**Expected value (mean)**
The long-run average value of a random variable.
- Discrete: E[X] = Σᵢ xᵢ · P(X = xᵢ).
- Continuous: E[X] = ∫ x · f(x) dx over the support.

Example: fair 3-sided die with outcomes {1, 2, 3}, each with P = 1/3 → E[X] = (1 + 2 + 3)/3 = 2.

**Variance**
Average squared deviation from the mean, measures spread.
- Var(X) = E[(X − E[X])²] = E[X²] − (E[X])²
- Standard deviation σ = √Var(X), in the same units as the data.

Example (same die): E[X²] = (1 + 4 + 9)/3 = 14/3; Var(X) = 14/3 − 4 = 2/3.

**Binomial shortcuts**
If X ~ Binomial(n, p): E[X] = np, Var(X) = np(1 − p).
Example (churn): n = 1000, p = 0.25 → expected 250 churns, Var = 187.5.

**Why this matters in AI**
- Expected value defines loss functions (e.g., MSE = expected squared error).
- In decision theory, pick actions that maximize expected utility.
- Reinforcement learning maximizes expected rewards.
- Variance quantifies prediction uncertainty — critical for overfitting diagnosis, risk modeling, Bayesian inference, and the bias–variance trade-off.
