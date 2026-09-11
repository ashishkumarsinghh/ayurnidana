import sqlite3
import os
import hashlib
import json

_DB_PATH = os.path.join(os.path.dirname(__file__), "../..", "data", "ayurnidana_v2.db")

def _db():
    os.makedirs(os.path.dirname(_DB_PATH), exist_ok=True)
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False, timeout=15.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        age INTEGER DEFAULT 35,
        gender TEXT DEFAULT 'Male',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS consultations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        chief_complaint TEXT,
        symptoms TEXT,
        primary_condition TEXT,
        sanskrit_name TEXT,
        dosha_scores TEXT,
        treatment_summary TEXT,
        case_sheet_md TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    return conn

def authenticate_user(identity: str, password: str):
    try:
        ph = hashlib.sha256(password.encode()).hexdigest()
        conn = _db()
        row = conn.execute(
            "SELECT * FROM users WHERE (username=? OR email=?) AND password_hash=?",
            (identity, identity, ph)
        ).fetchone()
        conn.close()
        if row: return True, "OK", dict(row)
        return False, "Incorrect username or password.", None
    except Exception as e:
        return False, f"Error: {e}", None

def register_user(username, email, password, full_name, age, gender):
    try:
        ph = hashlib.sha256(password.encode()).hexdigest()
        conn = _db()
        conn.execute(
            "INSERT INTO users (username,email,password_hash,full_name,age,gender) VALUES (?,?,?,?,?,?)",
            (username, email, ph, full_name, age, gender)
        )
        conn.commit()
        row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()
        return True, "Account created!", dict(row)
    except sqlite3.IntegrityError:
        return False, "Username or email already in use.", None
    except Exception as e:
        return False, f"Error: {e}", None

def save_consultation(user_id, chief_complaint, symptoms, primary_condition,
                      sanskrit_name, dosha_scores, treatment_summary, case_sheet_md):
    try:
        conn = _db()
        conn.execute(
            """INSERT INTO consultations
               (user_id,chief_complaint,symptoms,primary_condition,sanskrit_name,
                dosha_scores,treatment_summary,case_sheet_md)
               VALUES (?,?,?,?,?,?,?,?)""",
            (user_id, chief_complaint, json.dumps(symptoms), primary_condition,
             sanskrit_name, json.dumps(dosha_scores), treatment_summary, case_sheet_md)
        )
        conn.commit()
        cid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return cid
    except Exception:
        return None

def get_user_consultations(user_id):
    try:
        conn = _db()
        rows = conn.execute(
            "SELECT * FROM consultations WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
        conn.close()
        result = []
        for r in rows:
            d = dict(r)
            d["symptoms"]     = json.loads(d.get("symptoms") or "[]")
            d["dosha_scores"] = json.loads(d.get("dosha_scores") or "{}")
            result.append(d)
        return result
    except Exception:
        return []
