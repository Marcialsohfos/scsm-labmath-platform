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
