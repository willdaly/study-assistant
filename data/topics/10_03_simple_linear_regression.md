---
module: 10
section: "10.3"
title: "Simple Linear Regression"
---

Simple linear regression predicts an outcome y from a single predictor x by fitting a straight line.

**Model**
Y = β₀ + β₁ X + ε
- β₀: intercept — predicted y when x = 0 (baseline).
- β₁: slope — change in predicted y per one-unit increase in x.
- ε: random error.

**Interpreting the line**
ŷ = 50 + 5x → intercept 50 (predicted score with 0 study hours), slope 5 (each extra hour adds 5 points to the prediction).

**Least squares fit**
Pick β₀, β₁ to minimize the sum of squared residuals: Σ (yᵢ − ŷᵢ)². Squaring penalizes large errors and yields a smooth, differentiable objective.

For simple regression, the closed-form solution:
- β₁ = Σ(xᵢ − x̄)(yᵢ − ȳ) / Σ(xᵢ − x̄)²
- β₀ = ȳ − β₁ · x̄

**Making predictions**
Plug x into ŷ = β₀ + β₁ x. Example: x = 4 → ŷ = 70.

**Caveats**
- Predictions are reliable only within the range of training data (don't extrapolate far beyond).
- Point estimates don't convey uncertainty — pair with a prediction interval when decisions depend on precision.

**In AI**: foundational for forecasting, user-behavior modeling, and as a building block for more complex methods (multiple regression, logistic regression, neural-network output layers).
