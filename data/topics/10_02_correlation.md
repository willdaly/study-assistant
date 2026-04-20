---
module: 10
section: "10.2"
title: "Correlation"
---

Correlation measures the strength and direction of the linear relationship between two numerical variables.

**Pearson correlation coefficient (r)**
Always between −1 and +1.
- r = +1: perfect positive linear relationship.
- r = −1: perfect negative linear relationship.
- r = 0: no linear relationship.

Rough guidelines:
- |r| ≈ 0.8: strong.
- |r| ≈ 0.3: weak.
- |r| ≈ 0: none.

**Interpretation examples**
- Study hours and test score: r = 0.9 (strong positive).
- Social media hours and grades: r = −0.6 (moderate negative).

**Limitations**
- Only captures *linear* patterns. A perfectly quadratic relationship can have r ≈ 0.
- Correlation ≠ causation. Two variables can move together because of a common cause (confounder) or even by chance.

**Uses in AI**
1. **Feature selection**: variables strongly correlated with the target are promising predictors.
2. **Detecting multicollinearity**: features highly correlated with each other can distort regression coefficients; correlation matrices help spot and remove redundant inputs.
3. **Exploratory data analysis**: correlation heatmaps summarize relationships across many variables at once.

Scatter plots are the standard visualization — points clustering along an upward line indicate positive correlation; downward line, negative; random cloud, ≈ 0.
