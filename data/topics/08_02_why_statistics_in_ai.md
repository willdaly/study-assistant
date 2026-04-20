---
module: 8
section: "8.2"
title: "Why Statistics Matters in AI"
---

Statistics gives AI systems the tools to reason probabilistically rather than rigidly.

**Handling uncertainty**
Real-world data is noisy, incomplete, and unpredictable. Instead of saying "this will happen," a statistical AI system can say "this is likely to happen." Medical AI estimates disease probability from symptoms; a recommender ranks items by likelihood of preference.

**Estimation at the core of every model**
Models are trained on samples, not whole populations. The model must estimate parameters (like a regression slope, or a class probability) from observed data. Linear regression estimates slope and intercept; logistic regression estimates class-membership probabilities. Estimation is how an AI "learns from data" and generalizes to new cases.

**Performance evaluation relies on statistics**
- Metrics: accuracy, precision, recall, mean squared error — all summary statistics comparing predicted to actual.
- Sampling techniques: train-test splits and cross-validation test consistency across subsets.
- Reliability: confidence intervals and hypothesis tests distinguish real improvements from chance.

Without statistics, there's no rigorous way to tell whether one model is truly better than another or whether a model is ready for production.
