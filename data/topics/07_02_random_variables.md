---
module: 7
section: "7.2"
title: "Random Variables"
---

A random variable assigns a numerical value to each outcome of a random process. It turns abstract outcomes into numbers we can analyze mathematically.

**Example**
Flip a coin. Let X = 1 if heads, X = 0 if tails. Now we can compute probabilities, means, and variances.

**Discrete vs. continuous**
- Discrete: countable values — coin flips, emails per day, number of heads in 5 tosses. Described by a probability mass function (PMF).
- Continuous: any value in a range — temperature, height, transaction time. Described by a probability density function (PDF). For continuous X, P(X = exact value) = 0; only intervals have nonzero probability.

**Notation**
- Capital X, Y, Z for the random variable; lowercase x for specific values.
- P(X = x) reads "the probability X takes value x."

**Probability distribution (discrete example)**
Number of heads in 2 coin flips: X ∈ {0, 1, 2} with P = (0.25, 0.5, 0.25). Probabilities must sum to 1.

**Why this matters in AI**
- Prediction: will a user click? (discrete, Bernoulli).
- NLP: next word in a sentence (categorical over vocabulary).
- Image pixels (continuous intensities).
- Risk scoring: blood pressure, fraud scores (continuous).

Random variables let AI translate real-world randomness into structured data that can be learned from.
