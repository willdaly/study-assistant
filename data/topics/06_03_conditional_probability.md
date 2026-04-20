---
module: 6
section: "6.3"
title: "Conditional Probability and Independence"
---

Conditional probability updates the likelihood of an event given new information.

**Definition**
P(A | B) = P(A ∩ B) / P(B), provided P(B) > 0.

It answers: given B has occurred, what is the chance A also happens?

**Example — contingency table**
In a class of 100, 40 like tea; 25 like both tea and coffee. Then P(coffee | tea) = 25/40 = 0.625.

**Multiplication rule**
P(A ∩ B) = P(B) · P(A | B). Example: P(buy coffee) = 0.6, P(buy muffin | coffee) = 0.3 → P(both) = 0.18.

**Law of total probability**
If A₁, …, Aₙ partition the sample space: P(B) = Σᵢ P(B | Aᵢ) · P(Aᵢ). Example: 30% students with 80% laptop ownership, 70% non-students with 50% → P(laptop) = 0.8·0.3 + 0.5·0.7 = 0.59.

**Tree diagrams**
Multiply probabilities along a branch to get joint probabilities. For medical testing: P(has disease AND positive) = 0.01 · 0.90 = 0.009; P(no disease AND positive) = 0.99 · 0.05 = 0.0495.

**Independence**
Events A, B are independent iff P(A | B) = P(A), equivalently P(A ∩ B) = P(A) · P(B). Coin tosses are independent; drawing cards without replacement is not. Many ML models (e.g., Naive Bayes) assume conditional independence to simplify computation.
