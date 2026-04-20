"""
FastAPI app for the Study Assistant.

Serves:
  - GET  /api/topics                   list topics ranked by retention risk
  - GET  /api/topics/{id}              detail + questions (without the answer key)
  - GET  /api/topics/{id}/full         topic + questions WITH answers (for review UI)
  - POST /api/topics/{id}/attempt      record a quiz attempt; returns Bayesian update
  - GET  /api/math/data                (x, y) = (days_since_review, score) points across all attempts
  - GET  /api/math/regression          closed-form OLS fit over that data
  - POST /api/math/gradient            run gradient descent / SGD with chosen params
  - GET  /                             serves the frontend SPA
"""
from __future__ import annotations

import datetime as dt
import random
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import bayes, db, gradient, regression

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

app = FastAPI(title="Study Assistant")


# --- models ---------------------------------------------------------------

class AttemptIn(BaseModel):
    answers: list[int] = Field(..., description="Selected choice index per question (in the order served).")


class GDRequest(BaseModel):
    mode: str = Field("batch", pattern="^(batch|sgd)$")
    learning_rate: float = 0.01
    epochs: int = 2000
    sample_every: int = 10


# --- helpers --------------------------------------------------------------

def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _days_between(iso_a: str | None, iso_b: str) -> float:
    if not iso_a:
        return 0.0
    a = dt.datetime.fromisoformat(iso_a)
    b = dt.datetime.fromisoformat(iso_b)
    return max((b - a).total_seconds() / 86400.0, 0.0)


def _retention_now(topic: dict) -> float:
    """Apply time decay from last_reviewed_at to now for ranking."""
    if not topic.get("last_reviewed_at"):
        return topic.get("last_belief", 0.5)
    t = _days_between(topic["last_reviewed_at"], _now_iso())
    return bayes.retention_now(topic["last_belief"], topic["alpha"], t)


# --- API: topics ----------------------------------------------------------

@app.get("/api/topics")
def api_list_topics():
    topics = db.list_topics()
    out = []
    for t in topics:
        now_belief = _retention_now(t)
        days_since = _days_between(t.get("last_reviewed_at"), _now_iso()) if t.get("last_reviewed_at") else None
        out.append({
            "id": t["id"],
            "slug": t["slug"],
            "module": t["module"],
            "section": t["section"],
            "title": t["title"],
            "alpha": t["alpha"],
            "last_belief": t["last_belief"],
            "retention_now": now_belief,
            "days_since_review": days_since,
            "last_reviewed_at": t.get("last_reviewed_at"),
        })
    # Sort: topics never reviewed first (highest risk), then lowest retention first.
    out.sort(key=lambda r: (r["last_reviewed_at"] is not None, r["retention_now"]))
    return {"topics": out}


@app.get("/api/topics/{topic_id}")
def api_get_topic(topic_id: int):
    """Topic + its questions, minus the answer key. Used when rendering the quiz."""
    topic = db.get_topic(topic_id)
    if not topic:
        raise HTTPException(404, "Topic not found")
    questions = db.questions_for_topic(topic_id)
    # Shuffle questions and strip answers.
    random.shuffle(questions)
    served = [
        {"id": q["id"], "prompt": q["prompt"], "choices": q["choices"]}
        for q in questions
    ]
    return {
        "topic": {
            "id": topic["id"],
            "module": topic["module"],
            "section": topic["section"],
            "title": topic["title"],
            "content": topic["content"],
        },
        "questions": served,
    }


@app.get("/api/topics/{topic_id}/full")
def api_get_topic_full(topic_id: int):
    """Topic + questions with answers. For the review-after-submit view."""
    topic = db.get_topic(topic_id)
    if not topic:
        raise HTTPException(404, "Topic not found")
    return {
        "topic": dict(topic),
        "questions": db.questions_for_topic(topic_id),
        "attempts": db.attempts_for_topic(topic_id),
    }


@app.post("/api/topics/{topic_id}/attempt")
def api_record_attempt(topic_id: int, body: AttemptIn):
    topic = db.get_topic(topic_id)
    if not topic:
        raise HTTPException(404, "Topic not found")

    questions = db.questions_for_topic(topic_id)
    # The frontend fetched them in some shuffled order; we rely on it sending answers
    # keyed by question_id.  Simpler: require answers list same length as questions sorted by id.
    # To make this robust, accept either length-matched list by id order or explicit mapping.
    if len(body.answers) != len(questions):
        raise HTTPException(400, f"Expected {len(questions)} answers, got {len(body.answers)}")
    # Sort questions by id for a stable order, then score.
    questions_sorted = sorted(questions, key=lambda q: q["id"])
    correct = sum(1 for q, a in zip(questions_sorted, body.answers) if a == q["correct_index"])
    total = len(questions_sorted)
    score = correct / total if total else 0.0

    now = _now_iso()
    days_since = _days_between(topic.get("last_reviewed_at"), now)

    # Bayesian update: rebuild the belief from all (days, score) events on this topic.
    attempts = db.attempts_for_topic(topic_id)
    events = [bayes.Event(days_since_review=a["days_since_review"], quiz_score=a["score"]) for a in attempts]
    events.append(bayes.Event(days_since_review=days_since, quiz_score=score))
    belief = bayes.current_belief(events, alpha=topic["alpha"])

    # Persist.
    attempt_id = db.insert_attempt(topic_id, now, days_since, score, correct, total)
    db.update_topic_state(topic_id, belief, now, topic["alpha"])

    # Per-question feedback.
    feedback = []
    for q, a in zip(questions_sorted, body.answers):
        feedback.append({
            "question_id": q["id"],
            "prompt": q["prompt"],
            "choices": q["choices"],
            "selected": a,
            "correct_index": q["correct_index"],
            "is_correct": a == q["correct_index"],
            "explanation": q["explanation"],
        })

    return {
        "attempt_id": attempt_id,
        "score": score,
        "correct": correct,
        "total": total,
        "days_since_review": days_since,
        "belief_after": belief,
        "feedback": feedback,
    }


# --- API: math lab --------------------------------------------------------

@app.get("/api/math/data")
def api_math_data():
    """All quiz attempts as (x=days_since_review, y=score*100) for regression / GD."""
    rows = db.all_attempts()
    pts = [{"x": r["days_since_review"], "y": r["score"] * 100.0, "attempt_id": r["id"],
            "topic_id": r["topic_id"], "attempted_at": r["attempted_at"]} for r in rows]
    return {"points": pts, "n": len(pts)}


@app.get("/api/math/regression")
def api_math_regression():
    rows = db.all_attempts()
    xs = [r["days_since_review"] for r in rows]
    ys = [r["score"] * 100.0 for r in rows]
    f = regression.fit(xs, ys)
    if f is None:
        return {"ok": False, "reason": "Need at least 2 attempts with varying days_since_review."}
    return {
        "ok": True,
        "beta0": f.beta0, "beta1": f.beta1,
        "r": f.r, "r_squared": f.r_squared,
        "n": f.n,
        "x_mean": f.x_mean, "y_mean": f.y_mean,
    }


@app.post("/api/math/gradient")
def api_math_gradient(body: GDRequest):
    rows = db.all_attempts()
    xs = [r["days_since_review"] for r in rows]
    ys = [r["score"] * 100.0 for r in rows]
    if len(xs) < 2:
        return {"ok": False, "reason": "Need at least 2 attempts."}
    if body.mode == "batch":
        res = gradient.batch_gd(xs, ys, lr=body.learning_rate, epochs=body.epochs, sample_every=body.sample_every)
    else:
        res = gradient.sgd(xs, ys, lr=body.learning_rate, epochs=body.epochs, sample_every=body.sample_every)
    return {
        "ok": True,
        "mode": body.mode,
        "learning_rate": body.learning_rate,
        "epochs": body.epochs,
        "w": res.w, "b": res.b,
        "final_mse": res.final_mse,
        "history": res.history,
        "diverged": res.diverged,
    }


# --- frontend -------------------------------------------------------------

app.mount("/static", StaticFiles(directory=FRONTEND), name="static")


@app.get("/")
def index():
    return FileResponse(FRONTEND / "index.html")


# Bootstrap: ensure schema exists on import.
db.init_schema()
