"""SQLite helper functions to store and read chat logs."""
import sqlite3

DB_FILE = "chatbot.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS chat_logs (
               id           INTEGER PRIMARY KEY AUTOINCREMENT,
               session_id   TEXT NOT NULL,
               user_message TEXT NOT NULL,
               bot_reply    TEXT NOT NULL,
               intent       TEXT NOT NULL,
               confidence   REAL NOT NULL,
               created_at   TEXT DEFAULT CURRENT_TIMESTAMP
           )"""
    )
    conn.commit()
    conn.close()


def save_chat(session_id, user_message, bot_reply, intent, confidence):
    conn = get_connection()
    conn.execute(
        "INSERT INTO chat_logs (session_id, user_message, bot_reply, intent, confidence) VALUES (?, ?, ?, ?, ?)",
        (session_id, user_message, bot_reply, intent, round(confidence, 3)),
    )
    conn.commit()
    conn.close()


def get_last_question(session_id):
    """Last thing this user asked (used for follow-up questions)."""
    conn = get_connection()
    row = conn.execute(
        "SELECT user_message FROM chat_logs WHERE session_id = ? ORDER BY id DESC LIMIT 1",
        (session_id,),
    ).fetchone()
    conn.close()
    return row["user_message"] if row else None


def get_history(session_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT user_message, bot_reply FROM chat_logs WHERE session_id = ? ORDER BY id",
        (session_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_logs(limit=200):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM chat_logs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
