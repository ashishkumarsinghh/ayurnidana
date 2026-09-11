"""User Authentication, Registration, and Consultation History Persistence.
Built using standard library sqlite3 and cryptographically salted PBKDF2 hashing.
Requires zero external database servers; operates seamlessly locally and on Streamlit Cloud.
"""
import os
import sqlite3
import hashlib
import secrets
import json
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

# Default database path in project data folder or user home
DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, "ayurnidana.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30)
    conn.row_factory = sqlite3.Row
    # WAL mode: allows concurrent reads even during writes (essential for multi-user Streamlit)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=10000;")
    return conn

def init_db():
    """Initializes the database schema if not already present."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                full_name TEXT NOT NULL,
                age INTEGER DEFAULT 35,
                gender TEXT DEFAULT 'Male',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                chief_complaint TEXT,
                symptoms_json TEXT,
                primary_condition TEXT,
                sanskrit_name TEXT,
                dosha_scores_json TEXT,
                treatment_summary TEXT,
                case_sheet_md TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        conn.commit()

def _hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return key.hex(), salt

def register_user(
    username: str,
    email: str,
    password: str,
    full_name: str,
    age: int = 35,
    gender: str = "Male"
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Registers a new patient account."""
    username = username.strip().lower()
    email = email.strip().lower()
    full_name = full_name.strip()

    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long.", None
    if not email or "@" not in email:
        return False, "Please provide a valid email address.", None
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long.", None
    if not full_name:
        full_name = username.capitalize()

    init_db()
    pwd_hash, salt = _hash_password(password)

    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (username, email, password_hash, salt, full_name, age, gender)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (username, email, pwd_hash, salt, full_name, age, gender)
            )
            user_id = cursor.lastrowid
            conn.commit()
            
            user_data = {
                "id": user_id,
                "username": username,
                "email": email,
                "full_name": full_name,
                "age": age,
                "gender": gender
            }
            return True, "Account created successfully!", user_data
    except sqlite3.IntegrityError as e:
        err_msg = str(e).lower()
        if "username" in err_msg:
            return False, f"The username '{username}' is already taken. Please choose another.", None
        elif "email" in err_msg:
            return False, f"An account with email '{email}' already exists. Please sign in.", None
        return False, "An account with these details already exists.", None
    except Exception as e:
        return False, f"Registration failed: {str(e)}", None

def authenticate_user(username_or_email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """Authenticates a user via username or email."""
    init_db()
    query_str = username_or_email.strip().lower()

    if not query_str or not password:
        return False, "Please enter your username/email and password.", None

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, username, email, password_hash, salt, full_name, age, gender
            FROM users
            WHERE username = ? OR email = ?
            """,
            (query_str, query_str)
        )
        row = cursor.fetchone()
        if not row:
            return False, "No account found with that username or email.", None

        expected_hash, _ = _hash_password(password, row["salt"])
        if expected_hash != row["password_hash"]:
            return False, "Incorrect password. Please try again.", None

        user_data = {
            "id": row["id"],
            "username": row["username"],
            "email": row["email"],
            "full_name": row["full_name"],
            "age": row["age"],
            "gender": row["gender"]
        }
        return True, "Login successful!", user_data

def save_consultation(
    user_id: int,
    chief_complaint: str,
    symptoms: List[str],
    primary_condition: str,
    sanskrit_name: str,
    dosha_scores: Dict[str, float],
    treatment_summary: str,
    case_sheet_md: str
) -> Optional[int]:
    """Saves a consultation report to the user's permanent medical history."""
    init_db()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO consultations (
                    user_id, chief_complaint, symptoms_json, primary_condition,
                    sanskrit_name, dosha_scores_json, treatment_summary, case_sheet_md
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    chief_complaint,
                    json.dumps(symptoms),
                    primary_condition,
                    sanskrit_name,
                    json.dumps(dosha_scores),
                    treatment_summary,
                    case_sheet_md
                )
            )
            cid = cursor.lastrowid
            conn.commit()
            return cid
    except Exception:
        return None

def get_user_consultations(user_id: int) -> List[Dict[str, Any]]:
    """Retrieves all past consultations for the given user, latest first."""
    init_db()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, created_at, chief_complaint, symptoms_json, primary_condition,
                       sanskrit_name, dosha_scores_json, treatment_summary, case_sheet_md
                FROM consultations
                WHERE user_id = ?
                ORDER BY id DESC
                """,
                (user_id,)
            )
            rows = cursor.fetchall()
            results = []
            for r in rows:
                results.append({
                    "id": r["id"],
                    "created_at": r["created_at"],
                    "chief_complaint": r["chief_complaint"],
                    "symptoms": json.loads(r["symptoms_json"]) if r["symptoms_json"] else [],
                    "primary_condition": r["primary_condition"],
                    "sanskrit_name": r["sanskrit_name"],
                    "dosha_scores": json.loads(r["dosha_scores_json"]) if r["dosha_scores_json"] else {},
                    "treatment_summary": r["treatment_summary"],
                    "case_sheet_md": r["case_sheet_md"]
                })
            return results
    except Exception:
        return []

# Auto-initialize on import
init_db()
