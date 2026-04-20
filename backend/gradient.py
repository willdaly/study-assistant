"""
Part 3: Gradient descent (batch and stochastic) for the same linear model.

Loss (MSE):
    L(w, b) = (1/n) * sum_i (y_i - (w*x_i + b))^2

Gradients:
    dL/dw = (-2/n) * sum_i x_i * (y_i - (w*x_i + b))
    dL/db = (-2/n) * sum_i       (y_i - (w*x_i + b))

Batch GD computes gradients over the full dataset per epoch.
SGD shuffles and updates after every observation -- many more updates per epoch, but noisier.

Each function returns (history, final_w, final_b), where history is a list[dict]
with keys {epoch, w, b, mse} sampled every `sample_every` epochs so the frontend can plot it.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class GDResult:
    w: float
    b: float
    final_mse: float
    history: list[dict] = field(default_factory=list)  # {epoch, w, b, mse}
    diverged: bool = False


def mse(xs: list[float], ys: list[float], w: float, b: float) -> float:
    n = len(xs)
    if n == 0:
        return 0.0
    total = 0.0
    for x, y in zip(xs, ys):
        err = y - (w * x + b)
        total += err * err
    return total / n


def batch_gd(
    xs: list[float],
    ys: list[float],
    lr: float = 0.01,
    epochs: int = 2000,
    sample_every: int = 10,
    w0: float = 0.0,
    b0: float = 0.0,
) -> GDResult:
    n = len(xs)
    w, b = w0, b0
    history: list[dict] = []

    for epoch in range(epochs):
        dw = 0.0
        db = 0.0
        for x, y in zip(xs, ys):
            err = y - (w * x + b)
            dw += x * err
            db += err
        dw *= -2.0 / n
        db *= -2.0 / n

        w -= lr * dw
        b -= lr * db

        # Divergence guard: if loss blows up, bail out gracefully.
        if not (abs(w) < 1e9 and abs(b) < 1e9):
            current = float("inf")
            history.append({"epoch": epoch, "w": w, "b": b, "mse": current})
            return GDResult(w=w, b=b, final_mse=current, history=history, diverged=True)

        if epoch % sample_every == 0 or epoch == epochs - 1:
            history.append({"epoch": epoch, "w": w, "b": b, "mse": mse(xs, ys, w, b)})

    return GDResult(w=w, b=b, final_mse=mse(xs, ys, w, b), history=history)


def sgd(
    xs: list[float],
    ys: list[float],
    lr: float = 0.001,
    epochs: int = 2000,
    sample_every: int = 10,
    w0: float = 0.0,
    b0: float = 0.0,
    seed: int = 42,
) -> GDResult:
    n = len(xs)
    rng = random.Random(seed)
    w, b = w0, b0
    history: list[dict] = []
    indices = list(range(n))

    for epoch in range(epochs):
        rng.shuffle(indices)
        for i in indices:
            x, y = xs[i], ys[i]
            err = y - (w * x + b)
            # Per-sample gradient (no 1/n factor -- step is for a single point).
            dw = -2.0 * x * err
            db = -2.0 * err
            w -= lr * dw
            b -= lr * db

        if not (abs(w) < 1e9 and abs(b) < 1e9):
            current = float("inf")
            history.append({"epoch": epoch, "w": w, "b": b, "mse": current})
            return GDResult(w=w, b=b, final_mse=current, history=history, diverged=True)

        if epoch % sample_every == 0 or epoch == epochs - 1:
            history.append({"epoch": epoch, "w": w, "b": b, "mse": mse(xs, ys, w, b)})

    return GDResult(w=w, b=b, final_mse=mse(xs, ys, w, b), history=history)
