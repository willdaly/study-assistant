---
module: 8
section: "8.3"
title: "Sampling Methods"
---

A sample is a subset of a population. The way we choose it affects fairness, accuracy, and generalizability.

**Common sampling methods**

1. **Simple random sampling** — every individual has an equal probability of being selected, and every possible sample of a given size is equally likely. Fairness is maximal; selection bias is minimized. Used for train/test splits in ML.

2. **Stratified sampling** — divide the population into subgroups (strata) and sample from each separately. Useful when subgroups differ in important ways or when some groups are underrepresented. Produces balanced training sets and is key for fairness analysis.

3. **Systematic sampling** — pick every k-th element after a random start. Easy to implement on ordered data (log files, video frames), but can introduce bias if the data has a periodic pattern matching the interval.

**Sampling bias**
When some members are more likely to be selected than others, the sample misrepresents the population and downstream models inherit the bias.
- Self-selection bias: only motivated users respond to surveys.
- Undercoverage bias: dataset excludes certain demographics.
- Time bias: data collected at unrepresentative times.

A biased training set produces a biased model — e.g., a facial-recognition system trained mostly on light-skinned faces performs poorly on darker skin tones. Representative sampling is critical for trustworthy AI.
