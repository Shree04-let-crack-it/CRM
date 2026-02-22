import sqlite3
import uuid
from datetime import datetime
from config import DB_FILE


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # -------------------------
    # USERS TABLE
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            domain TEXT
        )
    """)

    # -------------------------
    # COMPLAINTS TABLE (UPDATED)
    # -------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id TEXT PRIMARY KEY,
            text TEXT NOT NULL,
            domain TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            username TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# --------------------------------------------------
# CREATE USER (Signup)
# --------------------------------------------------
def create_user(username, password, role, domain=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (id, username, password, role, domain)
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(uuid.uuid4()),
            username,
            password,
            role,
            domain
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


# --------------------------------------------------
# AUTHENTICATE USER (Login)
# --------------------------------------------------
def authenticate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, domain
        FROM users
        WHERE username=? AND password=?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()
    return user


# --------------------------------------------------
# INSERT COMPLAINT (UPDATED WITH USERNAME)
# --------------------------------------------------
def insert_complaint(text, domain, username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO complaints 
        (id, text, domain, priority, status, timestamp, username)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        str(uuid.uuid4()),
        text,
        domain,
        "Normal",
        "Pending",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        username
    ))

    conn.commit()
    conn.close()


# --------------------------------------------------
# GET ALL COMPLAINTS (Admin)
# --------------------------------------------------
def get_complaints():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, text, domain, priority, status, timestamp
        FROM complaints
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


# --------------------------------------------------
# GET COMPLAINTS BY USER (NEW FUNCTION)
# --------------------------------------------------
def get_complaints_by_user(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, text, domain, priority, status, timestamp
        FROM complaints
        WHERE username = ?
        ORDER BY timestamp DESC
    """, (username,))

    rows = cursor.fetchall()
    conn.close()
    return rows


# --------------------------------------------------
# GET COMPLAINTS BY DOMAIN (Officer)
# --------------------------------------------------
def get_complaints_by_domain(domain):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, text, domain, priority, status, timestamp
        FROM complaints
        WHERE domain = ?
        ORDER BY timestamp DESC
    """, (domain,))

    rows = cursor.fetchall()
    conn.close()
    return rows


# --------------------------------------------------
# UPDATE PRIORITY
# --------------------------------------------------
def update_priority(cid, priority):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints 
        SET priority = ?
        WHERE id = ?
    """, (priority, cid))

    conn.commit()
    conn.close()


# --------------------------------------------------
# UPDATE STATUS
# --------------------------------------------------
def update_status(cid, status):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE complaints 
        SET status = ?
        WHERE id = ?
    """, (status, cid))

    conn.commit()
    conn.close()


# --------------------------------------------------
# DELETE COMPLAINT
# --------------------------------------------------
def delete_complaint(cid):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM complaints
        WHERE id = ?
    """, (cid,))

    conn.commit()
    conn.close()
