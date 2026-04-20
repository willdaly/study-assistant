---
module: 10
section: "10.4"
title: "Evaluating Regression Models"
---

**Residuals**
For each observation, residual = y − ŷ.
- Positive residual → model underpredicted.
- Negative residual → model overpredicted.

Residual plots (residual vs. predicted) diagnose fit: random scatter = good; curved pattern = missing nonlinearity; fanning out = heteroscedasticity (non-constant error variance, which violates a regression assumption); huge residuals = potential outliers.

**Mean Squared Error (MSE)**
MSE = (1/n) Σ (yᵢ − ŷᵢ)²

- Squared so large errors are penalized more heavily.
- Lower MSE = better fit on average.
- MSE is the standard loss function minimized during model training (linear regression, neural networks, etc.).

Example: residuals (+5, −2, −2) → squared (25, 4, 4) → MSE = 33/3 = 11.

**R² (coefficient of determination)**
R² = 1 − SS_res / SS_tot, where SS_res = Σ(yᵢ − ŷᵢ)² and SS_tot = Σ(yᵢ − ȳ)².
- R² = 1: perfect fit.
- R² = 0: model no better than predicting ȳ.
- R² = 0.85 → 85% of the variance in y is explained by x.

**Caveats**
- High R² alone doesn't prove a good model — could be overfitting.
- Low R² doesn't always mean a bad model — some domains are inherently noisy.
- R² can't spot non-linearity, bias, or outliers; residual plots complement it.

Together, residual analysis + MSE + R² give you a rigorous picture of model quality.
