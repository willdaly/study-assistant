---
module: 6
section: "6.5"
title: "AI Applications of Probability"
---

Probability underpins how intelligent systems reason under uncertainty.

**Classification (Naive Bayes)**
Text classification like spam detection uses conditional probabilities: P(Spam | "lottery") = P("lottery" | Spam) · P(Spam) / P("lottery"). Naive Bayes assumes features are conditionally independent given the class, which is often a useful simplification.

**Medical diagnosis and risk assessment**
Systems combine disease prevalence (prior) with test results and symptoms (likelihoods) to produce posterior diagnostic probabilities in real time.

**Recommendation systems**
Netflix, Amazon and others update the probability you'll like an item after each interaction, often using Bayesian updating or probabilistic matrix factorization.

**Key takeaways**
- AI uses probability to make decisions under uncertainty with noisy, incomplete data.
- Conditional probability and Bayes' Theorem are embedded in many algorithms.
- Even simple models (Naive Bayes) rely on these concepts — they're foundational.
- Understanding probability helps you build, debug, and interpret AI models with confidence.
