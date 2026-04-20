---
module: 7
section: "7.3"
title: "Common Distributions"
---

**Binomial distribution — counts of successes in n trials**
Each trial has two outcomes (success/failure) with probability p, trials are independent. PMF: P(X = k) = C(n, k) · pᵏ · (1 − p)ⁿ⁻ᵏ.
Example: show ad to 10 users each with p = 0.3; P(exactly 3 clicks) ≈ 0.267.
Mean = np, variance = np(1 − p).
Used in: click prediction, A/B testing, success-rate modeling, logistic regression foundations.

**Normal (Gaussian) distribution — continuous bell curve**
Defined by mean μ and variance σ². Symmetric around μ.
Empirical rule: ≈68% of values within μ ± σ, ≈95% within μ ± 2σ, ≈99.7% within μ ± 3σ.
Central Limit Theorem says averages of many random variables tend to be normal — which justifies its use everywhere.
Used in: sensor noise, linear regression errors, neural network weight initialization, Gaussian Naive Bayes.

**Exponential distribution — waiting times**
Describes time between events in a Poisson process. Parameter λ = rate of events per unit time.
P(T > t) = e^(−λt), mean = 1/λ.
Memoryless: future probabilities don't depend on past waiting.
Example: website gets 6 visits/hour → P(next visit takes > 15 minutes) = e^(−1.5) ≈ 0.223.
Used in: survival/failure prediction, queuing systems, reinforcement-learning event timing.
