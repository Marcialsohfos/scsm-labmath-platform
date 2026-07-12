"""
db.py — Couche de persistance légère (SQLite) pour la plateforme SCSM Group / Lab_Math.

Tables :
- registrations : déclarations de paiement des apprenants (locked/unlocked par l'admin)
- settings      : paires clé/valeur (chemins des logos, textes de contact modifiables, etc.)
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "platform.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


_initialized = False


def ensure_init():
    """Idempotent safety net: creates tables on first use if init_db() wasn't
    called yet (e.g. a fresh deployment with no existing platform.db)."""
    global _initialized
    if not _initialized:
        init_db()
        _initialized = True


def init_db():
    conn = get_conn()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS registrations (
            email TEXT PRIMARY KEY,
            full_name TEXT,
            phone TEXT,
            method TEXT,
            reference TEXT,
            amount TEXT,
            unlocked INTEGER DEFAULT 0,
            created_at TEXT,
            unlocked_at TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title_fr TEXT NOT NULL,
            title_en TEXT,
            description_fr TEXT,
            description_en TEXT,
            order_index INTEGER DEFAULT 0,
            created_at TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS module_resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_id INTEGER NOT NULL,
            type TEXT NOT NULL,
            title TEXT,
            order_index INTEGER DEFAULT 0,
            file_path TEXT,
            external_url TEXT,
            text_content TEXT,
            language TEXT,
            starter_code TEXT,
            quiz_json TEXT,
            created_at TEXT,
            FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS progress (
            email TEXT NOT NULL,
            resource_id INTEGER NOT NULL,
            completed_at TEXT,
            score TEXT,
            PRIMARY KEY (email, resource_id)
        )
        """
    )
    conn.commit()
    conn.close()


# ---------------- Registrations ----------------

def add_registration(email, full_name, phone, method, reference, amount):
    ensure_init()
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO registrations (email, full_name, phone, method, reference, amount, unlocked, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 0, ?)
        ON CONFLICT(email) DO UPDATE SET
            full_name=excluded.full_name,
            phone=excluded.phone,
            method=excluded.method,
            reference=excluded.reference,
            amount=excluded.amount,
            created_at=excluded.created_at
        """,
        (email.strip().lower(), full_name, phone, method, reference, amount, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def get_registration(email):
    ensure_init()
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM registrations WHERE email = ?", (email.strip().lower(),)
    ).fetchone()
    conn.close()
    return row


def list_registrations():
    ensure_init()
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM registrations ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return rows


def set_unlocked(email, unlocked: bool):
    ensure_init()
    conn = get_conn()
    conn.execute(
        "UPDATE registrations SET unlocked = ?, unlocked_at = ? WHERE email = ?",
        (1 if unlocked else 0, datetime.utcnow().isoformat() if unlocked else None, email.strip().lower()),
    )
    conn.commit()
    conn.close()


# ---------------- Settings (logos, textes) ----------------

def set_setting(key, value):
    ensure_init()
    conn = get_conn()
    conn.execute(
        "INSERT INTO settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )
    conn.commit()
    conn.close()


def get_setting(key, default=None):
    ensure_init()
    conn = get_conn()
    row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


# ---------------- Modules ----------------

def add_module(title_fr, title_en, description_fr, description_en):
    ensure_init()
    conn = get_conn()
    max_order = conn.execute("SELECT COALESCE(MAX(order_index), -1) AS m FROM modules").fetchone()["m"]
    cur = conn.execute(
        """
        INSERT INTO modules (title_fr, title_en, description_fr, description_en, order_index, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title_fr, title_en, description_fr, description_en, max_order + 1, datetime.utcnow().isoformat()),
    )
    conn.commit()
    module_id = cur.lastrowid
    conn.close()
    return module_id


def update_module(module_id, title_fr, title_en, description_fr, description_en):
    ensure_init()
    conn = get_conn()
    conn.execute(
        """
        UPDATE modules SET title_fr = ?, title_en = ?, description_fr = ?, description_en = ?
        WHERE id = ?
        """,
        (title_fr, title_en, description_fr, description_en, module_id),
    )
    conn.commit()
    conn.close()


def delete_module(module_id):
    ensure_init()
    conn = get_conn()
    conn.execute("DELETE FROM module_resources WHERE module_id = ?", (module_id,))
    conn.execute("DELETE FROM modules WHERE id = ?", (module_id,))
    conn.commit()
    conn.close()


def list_modules():
    ensure_init()
    conn = get_conn()
    rows = conn.execute("SELECT * FROM modules ORDER BY order_index ASC, id ASC").fetchall()
    conn.close()
    return rows


def get_module(module_id):
    ensure_init()
    conn = get_conn()
    row = conn.execute("SELECT * FROM modules WHERE id = ?", (module_id,)).fetchone()
    conn.close()
    return row


def move_module(module_id, direction):
    """direction: -1 (up) or +1 (down) — swaps order_index with the neighbouring module."""
    ensure_init()
    modules = list_modules()
    ids = [m["id"] for m in modules]
    if module_id not in ids:
        return
    idx = ids.index(module_id)
    swap_idx = idx + direction
    if swap_idx < 0 or swap_idx >= len(modules):
        return
    conn = get_conn()
    a, b = modules[idx], modules[swap_idx]
    conn.execute("UPDATE modules SET order_index = ? WHERE id = ?", (b["order_index"], a["id"]))
    conn.execute("UPDATE modules SET order_index = ? WHERE id = ?", (a["order_index"], b["id"]))
    conn.commit()
    conn.close()


# ---------------- Module resources (vidéos, cours, PDF, sandbox, quiz) ----------------

def add_resource(module_id, type_, title, file_path=None, external_url=None,
                  text_content=None, language=None, starter_code=None, quiz_json=None):
    ensure_init()
    conn = get_conn()
    max_order = conn.execute(
        "SELECT COALESCE(MAX(order_index), -1) AS m FROM module_resources WHERE module_id = ?",
        (module_id,),
    ).fetchone()["m"]
    cur = conn.execute(
        """
        INSERT INTO module_resources
            (module_id, type, title, order_index, file_path, external_url,
             text_content, language, starter_code, quiz_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (module_id, type_, title, max_order + 1, file_path, external_url,
         text_content, language, starter_code, quiz_json, datetime.utcnow().isoformat()),
    )
    conn.commit()
    resource_id = cur.lastrowid
    conn.close()
    return resource_id


def list_resources(module_id):
    ensure_init()
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM module_resources WHERE module_id = ? ORDER BY order_index ASC, id ASC",
        (module_id,),
    ).fetchall()
    conn.close()
    return rows


def count_resources(module_id):
    ensure_init()
    conn = get_conn()
    row = conn.execute(
        "SELECT COUNT(*) AS c FROM module_resources WHERE module_id = ?", (module_id,)
    ).fetchone()
    conn.close()
    return row["c"]


def delete_resource(resource_id):
    ensure_init()
    conn = get_conn()
    conn.execute("DELETE FROM module_resources WHERE id = ?", (resource_id,))
    conn.execute("DELETE FROM progress WHERE resource_id = ?", (resource_id,))
    conn.commit()
    conn.close()


# ---------------- Progression des apprenants ----------------

def mark_progress(email, resource_id, score=None):
    ensure_init()
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO progress (email, resource_id, completed_at, score)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(email, resource_id) DO UPDATE SET
            completed_at = excluded.completed_at,
            score = excluded.score
        """,
        (email.strip().lower(), resource_id, datetime.utcnow().isoformat(), score),
    )
    conn.commit()
    conn.close()


def unmark_progress(email, resource_id):
    ensure_init()
    conn = get_conn()
    conn.execute(
        "DELETE FROM progress WHERE email = ? AND resource_id = ?",
        (email.strip().lower(), resource_id),
    )
    conn.commit()
    conn.close()


def is_completed(email, resource_id):
    ensure_init()
    conn = get_conn()
    row = conn.execute(
        "SELECT 1 FROM progress WHERE email = ? AND resource_id = ?",
        (email.strip().lower(), resource_id),
    ).fetchone()
    conn.close()
    return row is not None


def get_progress_score(email, resource_id):
    ensure_init()
    conn = get_conn()
    row = conn.execute(
        "SELECT score FROM progress WHERE email = ? AND resource_id = ?",
        (email.strip().lower(), resource_id),
    ).fetchone()
    conn.close()
    return row["score"] if row else None


def module_progress_ratio(email, module_id):
    """Retourne (nb_terminés, nb_total) pour un module donné et un apprenant."""
    ensure_init()
    conn = get_conn()
    total = conn.execute(
        "SELECT COUNT(*) AS c FROM module_resources WHERE module_id = ?", (module_id,)
    ).fetchone()["c"]
    done = conn.execute(
        """
        SELECT COUNT(*) AS c FROM progress p
        JOIN module_resources r ON r.id = p.resource_id
        WHERE r.module_id = ? AND p.email = ?
        """,
        (module_id, email.strip().lower()),
    ).fetchone()["c"]
    conn.close()
    return done, total
