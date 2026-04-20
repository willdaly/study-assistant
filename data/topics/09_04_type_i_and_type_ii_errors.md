---
module: 9
section: "9.4"
title: "Type I and Type II Errors"
---

Two ways to be wrong in hypothesis testing:

**Type I error (false positive, α)**
Rejecting H₀ when H₀ is actually true. Probability = α, the significance level. In spam filtering, a legitimate email marked as spam. In medicine, a healthy patient flagged as sick.

**Type II error (false negative, β)**
Failing to reject H₀ when H₀ is actually false. Missing a real effect. In spam filtering, a phishing email that slips through. In medicine, a missed diagnosis.

**Decision table**

|                   | H₀ true         | H₀ false         |
| ----------------- | --------------- | ---------------- |
| Reject H₀         | Type I error    | Correct decision |
| Fail to reject H₀ | Correct decision| Type II error    |

**Power**
Power = 1 − β = probability of correctly rejecting H₀ when it's false. A well-designed test has power ≥ 0.80. Larger n, larger true effect, or larger α all increase power.

**The trade-off**
Lowering α reduces false positives but raises false negatives. You can't minimize both simultaneously — you balance them based on which error is more costly in context.

**Application choices**
- Healthcare cancer screening: minimize type II errors (missing disease is life-threatening). Accept more false positives (followup tests).
- Autopilot / safety-critical control: prioritize avoiding type I errors (don't act on noise).

Responsible AI design picks which error matters more for the users and use case at hand.
