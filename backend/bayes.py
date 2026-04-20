"""
Part 1: Bayesian retention belief.

Per-topic posterior P(retains | evidence), where evidence is a sequence of (days_since_review, quiz_score) events.

Model
-----
Prior at the start of a study session: P(R) = 0.5 (flat).
After each quiz at time t (days since last review), the time-decayed prior is
    P(R_t) = P(R) * exp(-alpha * t)        (exponential forgetting)
where alpha is the per-topic decay rate.

Likelihood uses the quiz score s in [0, 1]:
    P(pass | R)     = s_max (high if retained) -- we treat the observed score as the likelihood of passing
    P(pass | ¬R)    = 1 - s_max (guess rate if not retained)

We use a smoothed form so that partial-credit scores update the belief smoothly.

The posterior is:
    P(R | s) = s * P(R_t) / ( s * P(R_t) + (1 - s) * (1 - P(R_t)) )

This matches the formulation in Part 1 / Part 2 of the write-up: Bayesian update combined with exponential time decay.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class Event:
    days_since_review: float   # t (days since the previous review for this topic)
    quiz_score: float          # in [0, 1]


def time_decayed_prior(prior: float, alpha: float, t_days: float) -> float:
    """Exponential forgetting: belief decays from `prior` toward 0 over time."""
    if t_days < 0:
        t_days = 0.0
    return prior * math.exp(-alpha * t_days)


def posterior(prior_retained: float, quiz_score: float) -> float:
    """Apply one Bayesian update given a quiz score in [0, 1]."""
    s = max(min(quiz_score, 1.0), 0.0)
    p = max(min(prior_retained, 1.0), 0.0)
    num = s * p
    denom = s * p + (1.0 - s) * (1.0 - p)
    if denom <= 0:
        return p
    return num / denom


def current_belief(events: list[Event], alpha: float = 0.05, base_prior: float = 0.5) -> float:
    """
    Run the full Bayesian + time-decay process over an ordered list of events.
    The last event's days_since_review represents "now - last review".

    Returns P(retains) ∈ [0, 1].
    """
    p = base_prior
    for ev in events:
        p = time_decayed_prior(p, alpha, ev.days_since_review)
        p = posterior(p, ev.quiz_score)
    return p


def retention_now(last_belief: float, alpha: float, days_since_last_update: float) -> float:
    """Apply only time decay, e.g. for ranking a topic on the dashboard."""
    return time_decayed_prior(last_belief, alpha, days_since_last_update)
