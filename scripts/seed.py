"""
Seed the database from data/topics/*.md.

For each topic:
  1. Parse the front-matter + body.
  2. Upsert into the `topics` table.
  3. If the topic has no questions yet, ask Claude Haiku 4.5 to generate 4 multiple-choice questions
     based on the topic content. Uses prompt caching on the system prompt so a re-run costs less.

Requires ANTHROPIC_API_KEY in the environment. The script skips question generation if the
env var is missing, letting you seed content without an API key and add questions later.

Run:
    python scripts/seed.py
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

from backend import db  # noqa: E402

TOPIC_DIR = ROOT / "data" / "topics"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)


def parse_topic_file(path: Path) -> dict:
    text = path.read_text()
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"{path} is missing front-matter")
    fm_raw, body = m.group(1), m.group(2).strip()
    fm = {}
    for line in fm_raw.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return {
        "slug": path.stem,
        "module": int(fm.get("module", 0)),
        "section": fm.get("section", ""),
        "title": fm.get("title", path.stem),
        "content": body,
    }


SYSTEM_PROMPT = """You are an expert in mathematical concepts for AI (AAI 5015 curriculum).
You write high-quality multiple-choice study questions that test understanding, not recall.

Rules:
- Exactly 4 choices (A, B, C, D).
- Exactly one correct choice.
- Distractors must be plausible and reflect common misunderstandings, not obviously wrong.
- Write a short (1-3 sentence) explanation of why the correct answer is right.
- Cover different facets of the topic: definition, calculation/application, and interpretation.
- Do not reference "the passage" or "the text" -- write as standalone questions.

Respond with ONLY a JSON object matching this schema:
{
  "questions": [
    {"prompt": str, "choices": [str, str, str, str], "correct_index": 0-3, "explanation": str},
    ...
  ]
}
"""


def generate_questions(client, topic: dict, n_questions: int = 4) -> list[dict]:
    user_msg = (
        f"Topic: {topic['title']} (Module {topic['module']}, Section {topic['section']})\n\n"
        f"Source content:\n{topic['content']}\n\n"
        f"Generate exactly {n_questions} multiple-choice questions."
    )
    # Cache the system prompt -- reused across every call.
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2048,
        system=[
            {"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}
        ],
        messages=[{"role": "user", "content": user_msg}],
    )
    text = "".join(block.text for block in msg.content if block.type == "text").strip()
    # Strip code fences if present.
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    data = json.loads(text)
    return data["questions"]


def upsert_topic(topic: dict) -> int:
    with db.tx() as conn:
        row = conn.execute("SELECT id FROM topics WHERE slug = ?", (topic["slug"],)).fetchone()
        if row:
            conn.execute(
                "UPDATE topics SET module=?, section=?, title=?, content=? WHERE id=?",
                (topic["module"], topic["section"], topic["title"], topic["content"], row["id"]),
            )
            return row["id"]
        cur = conn.execute(
            "INSERT INTO topics(slug, module, section, title, content) VALUES (?, ?, ?, ?, ?)",
            (topic["slug"], topic["module"], topic["section"], topic["title"], topic["content"]),
        )
        return cur.lastrowid


def topic_has_questions(topic_id: int) -> bool:
    with db.connect() as conn:
        row = conn.execute("SELECT COUNT(*) AS n FROM questions WHERE topic_id = ?", (topic_id,)).fetchone()
        return row["n"] > 0


def insert_questions(topic_id: int, questions: list[dict]) -> None:
    with db.tx() as conn:
        for q in questions:
            conn.execute(
                "INSERT INTO questions(topic_id, prompt, choices_json, correct_index, explanation) "
                "VALUES (?, ?, ?, ?, ?)",
                (topic_id, q["prompt"], json.dumps(q["choices"]), int(q["correct_index"]), q["explanation"]),
            )


def main() -> None:
    db.init_schema()

    files = sorted(TOPIC_DIR.glob("*.md"))
    if not files:
        print(f"No topic files in {TOPIC_DIR}")
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    client = None
    if api_key:
        try:
            from anthropic import Anthropic
        except ImportError:
            print("anthropic package not installed; run `pip install -r requirements.txt`")
            return
        client = Anthropic(api_key=api_key)
    else:
        print("(!) ANTHROPIC_API_KEY not set — will seed topic content but skip question generation.")

    for f in files:
        topic = parse_topic_file(f)
        topic_id = upsert_topic(topic)
        print(f"✓ {topic['section']:<5} {topic['title']}  (id={topic_id})")

        if client and not topic_has_questions(topic_id):
            try:
                questions = generate_questions(client, topic, n_questions=4)
                insert_questions(topic_id, questions)
                print(f"   → generated {len(questions)} questions")
            except Exception as exc:  # noqa: BLE001
                print(f"   ! question generation failed: {exc}")
        elif client:
            print("   (already has questions; skipping)")

    print("\nDone.")


if __name__ == "__main__":
    main()
