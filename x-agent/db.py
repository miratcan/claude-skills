"""SQLite database for X agent — strategy, posts, engagement, retrospectives."""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "db" / "x-agent.db"
SEED_STRATEGY = Path(__file__).parent / "seed-strategy.json"


def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS strategies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            content TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 0,
            parent_id INTEGER REFERENCES strategies(id)
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            x_post_url TEXT,
            content TEXT NOT NULL,
            post_type TEXT NOT NULL,
            strategy_id INTEGER NOT NULL REFERENCES strategies(id),
            posted_at TEXT
        );

        CREATE TABLE IF NOT EXISTS engagement_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL REFERENCES posts(id),
            checked_at TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            retweets INTEGER DEFAULT 0,
            replies INTEGER DEFAULT 0,
            quote_tweets INTEGER DEFAULT 0,
            impressions INTEGER DEFAULT 0,
            photo_replies_count INTEGER DEFAULT 0,
            reply_samples TEXT DEFAULT '[]'
        );

        CREATE TABLE IF NOT EXISTS retrospectives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            period_start TEXT NOT NULL,
            period_end TEXT NOT NULL,
            posts_analyzed INTEGER NOT NULL,
            findings TEXT NOT NULL,
            strategy_changes TEXT NOT NULL,
            new_strategy_id INTEGER REFERENCES strategies(id)
        );
    """)
    conn.commit()

    # Seed strategy if none exists
    active = conn.execute(
        "SELECT id FROM strategies WHERE active = 1"
    ).fetchone()
    if not active:
        seed = json.loads(SEED_STRATEGY.read_text())
        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            "INSERT INTO strategies (created_at, content, active) VALUES (?, ?, 1)",
            (now, json.dumps(seed, ensure_ascii=False)),
        )
        conn.commit()

    conn.close()


def get_active_strategy(conn: sqlite3.Connection) -> dict:
    row = conn.execute(
        "SELECT * FROM strategies WHERE active = 1 ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if not row:
        raise RuntimeError("No active strategy found. Run init_db() first.")
    return {**dict(row), "content": json.loads(row["content"])}


def save_post(conn: sqlite3.Connection, content: str, post_type: str,
              strategy_id: int, x_post_url: str | None = None) -> int:
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        """INSERT INTO posts (created_at, x_post_url, content, post_type, strategy_id, posted_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (now, x_post_url, content, post_type, strategy_id, now),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def save_engagement(conn: sqlite3.Connection, post_id: int, **metrics) -> int:
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        """INSERT INTO engagement_snapshots
           (post_id, checked_at, likes, retweets, replies, quote_tweets,
            impressions, photo_replies_count, reply_samples)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            post_id, now,
            metrics.get("likes", 0),
            metrics.get("retweets", 0),
            metrics.get("replies", 0),
            metrics.get("quote_tweets", 0),
            metrics.get("impressions", 0),
            metrics.get("photo_replies_count", 0),
            json.dumps(metrics.get("reply_samples", []), ensure_ascii=False),
        ),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def get_posts_since_last_retro(conn: sqlite3.Connection) -> list[dict]:
    last_retro = conn.execute(
        "SELECT period_end FROM retrospectives ORDER BY id DESC LIMIT 1"
    ).fetchone()
    if last_retro:
        rows = conn.execute(
            "SELECT * FROM posts WHERE created_at > ? ORDER BY created_at",
            (last_retro["period_end"],),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM posts ORDER BY created_at"
        ).fetchall()
    return [dict(r) for r in rows]


def get_latest_engagement(conn: sqlite3.Connection, post_id: int) -> dict | None:
    row = conn.execute(
        """SELECT * FROM engagement_snapshots
           WHERE post_id = ? ORDER BY checked_at DESC LIMIT 1""",
        (post_id,),
    ).fetchone()
    return dict(row) if row else None


def count_posts_since_last_retro(conn: sqlite3.Connection) -> int:
    return len(get_posts_since_last_retro(conn))


def save_retrospective(conn: sqlite3.Connection, period_start: str,
                       period_end: str, posts_analyzed: int,
                       findings: dict, strategy_changes: dict,
                       new_strategy_id: int | None = None) -> int:
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        """INSERT INTO retrospectives
           (created_at, period_start, period_end, posts_analyzed,
            findings, strategy_changes, new_strategy_id)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            now, period_start, period_end, posts_analyzed,
            json.dumps(findings, ensure_ascii=False),
            json.dumps(strategy_changes, ensure_ascii=False),
            new_strategy_id,
        ),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


def create_new_strategy(conn: sqlite3.Connection, content: dict,
                        parent_id: int) -> int:
    # Deactivate current
    conn.execute("UPDATE strategies SET active = 0 WHERE active = 1")
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        """INSERT INTO strategies (created_at, content, active, parent_id)
           VALUES (?, ?, 1, ?)""",
        (now, json.dumps(content, ensure_ascii=False), parent_id),
    )
    conn.commit()
    assert cur.lastrowid is not None
    return cur.lastrowid


if __name__ == "__main__":
    init_db()
    conn = get_db()
    strategy = get_active_strategy(conn)
    import pprint
    print("DB initialized. Active strategy:")
    pprint.pprint(strategy["content"])
    print(f"\nDB location: {DB_PATH}")
    conn.close()
