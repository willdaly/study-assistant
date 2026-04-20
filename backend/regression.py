"""
Part 2: Linear regression — predict quiz score from days since last review.

Uses the closed-form (ordinary least squares) solution for simple linear regression,
matching the derivation in Part 2 of the write-up:
    beta_1 = sum((x - x_bar)(y - y_bar)) / sum((x - x_bar)^2)
    beta_0 = y_bar - beta_1 * x_bar

Also computes Pearson r and R^2.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Fit:
    beta0: float
    beta1: float
    r: float
    r_squared: float
    n: int
    x_mean: float
    y_mean: float


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else 0.0


def fit(xs: list[float], ys: list[float]) -> Fit | None:
    """Fit y = beta0 + beta1 * x. Returns None if we don't have enough data or x has no variance."""
    n = len(xs)
    if n < 2 or len(ys) != n:
        return None

    x_bar = mean(xs)
    y_bar = mean(ys)

    sxx = sum((x - x_bar) ** 2 for x in xs)
    syy = sum((y - y_bar) ** 2 for y in ys)
    sxy = sum((x - x_bar) * (y - y_bar) for x, y in zip(xs, ys))

    if sxx == 0:
        return None

    beta1 = sxy / sxx
    beta0 = y_bar - beta1 * x_bar

    r = sxy / (sxx * syy) ** 0.5 if sxx > 0 and syy > 0 else 0.0
    r_squared = r * r

    return Fit(beta0=beta0, beta1=beta1, r=r, r_squared=r_squared, n=n, x_mean=x_bar, y_mean=y_bar)


def predict(f: Fit, x: float) -> float:
    return f.beta0 + f.beta1 * x
