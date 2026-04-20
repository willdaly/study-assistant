---
module: 9
section: "9.2"
title: "Confidence Intervals"
---

A confidence interval (CI) is a range around a point estimate that likely contains the true population parameter, expressing uncertainty.

**Structure**
CI = point estimate ± margin of error

Margin of error depends on:
- **Standard error** — how much the estimate varies across samples. Falls with larger n.
- **Critical value** — from the normal distribution (z) when n is large or σ known, or from the t-distribution when n is small or σ unknown.

**CI for a mean** (σ known): x̄ ± z_{α/2} · (σ/√n).

**CI for a proportion**: p̂ ± z_{α/2} · √( p̂ (1 − p̂) / n ).

**The Central Limit Theorem (CLT)**
For large enough n (typically ≥ 30), the sampling distribution of x̄ is approximately normal regardless of the population distribution. This is why we can use z- or t-based intervals even for non-normal data.

**Correct interpretation**
A 95% CI (4.8, 5.6) does NOT mean "there's a 95% chance the true mean is in this specific interval." Rather, if we repeated the sampling process many times, about 95% of such constructed intervals would contain the true value. The method is right 95% of the time; your particular interval either contains μ or doesn't.

**Used in AI for**: comparing model accuracies, reporting metric uncertainty, A/B test readouts.
