"""SQLite connection + helpers. Single-process dev app -- no pooling needed."""
from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.environ.get("STUDY_DB", ROOT / "data" / "study.db"))
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_schema() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA_PATH.read_text())


@contextmanager
def tx():
    conn = connect()
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# --- Topic queries ---------------------------------------------------------

def list_topics() -> list[dict]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM topics ORDER BY module, section"
        ).fetchall()
        return [dict(r) for r in rows]


def get_topic(topic_id: int) -> dict | None:
    with connect() as conn:
        row = conn.execute("SELECT * FROM topics WHERE id = ?", (topic_id,)).fetchone()
        return dict(row) if row else None


def update_topic_state(topic_id: int, last_belief: float, last_reviewed_at: str, alpha: float) -> None:
    with tx() as conn:
        conn.execute(
            "UPDATE topics SET last_belief = ?, last_reviewed_at = ?, alpha = ? WHERE id = ?",
            (last_belief, last_reviewed_at, alpha, topic_id),
        )


# --- Question queries ------------------------------------------------------

def questions_for_topic(topic_id: int) -> list[dict]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT id, topic_id, prompt, choices_json, correct_index, explanation "
            "FROM questions WHERE topic_id = ?",
            (topic_id,),
        ).fetchall()
    out = []
    for r in rows:
        d = dict(r)
        d["choices"] = json.loads(d.pop("choices_json"))
        out.append(d)
    return out


# --- Attempt queries -------------------------------------------------------

def insert_attempt(topic_id: int, attempted_at: str, days_since_review: float,
                   score: float, correct_count: int, total_count: int) -> int:
    with tx() as conn:
        cur = conn.execute(
            "INSERT INTO quiz_attempts(topic_id, attempted_at, days_since_review, "
            "score, correct_count, total_count) VALUES (?, ?, ?, ?, ?, ?)",
            (topic_id, attempted_at, days_since_review, score, correct_count, total_count),
        )
        return cur.lastrowid


def attempts_for_topic(topic_id: int) -> list[dict]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM quiz_attempts WHERE topic_id = ? ORDER BY attempted_at",
            (topic_id,),
        ).fetchall()
        return [dict(r) for r in rows]


def all_attempts() -> list[dict]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM quiz_attempts ORDER BY attempted_at"
        ).fetchall()
        return [dict(r) for r in rows]
