-- Study Assistant schema

CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT NOT NULL UNIQUE,
    module INTEGER NOT NULL,
    section TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    -- Per-topic decay rate alpha (learned via gradient descent on (days, score) data).
    alpha REAL NOT NULL DEFAULT 0.05,
    -- Last Bayesian belief P(retained), updated after each quiz attempt.
    last_belief REAL NOT NULL DEFAULT 0.5,
    last_reviewed_at TEXT  -- ISO8601; null until first quiz
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    prompt TEXT NOT NULL,
    -- A, B, C, D choices stored as JSON array of strings.
    choices_json TEXT NOT NULL,
    correct_index INTEGER NOT NULL,
    explanation TEXT NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_questions_topic ON questions(topic_id);

CREATE TABLE IF NOT EXISTS quiz_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    attempted_at TEXT NOT NULL,           -- ISO8601 UTC
    days_since_review REAL NOT NULL,      -- computed at attempt time vs. topic.last_reviewed_at
    score REAL NOT NULL,                  -- fraction in [0, 1]
    correct_count INTEGER NOT NULL,
    total_count INTEGER NOT NULL,
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_attempts_topic ON quiz_attempts(topic_id);
CREATE INDEX IF NOT EXISTS idx_attempts_time ON quiz_attempts(attempted_at);
