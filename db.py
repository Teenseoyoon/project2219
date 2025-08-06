import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            job TEXT,
            hp INTEGER,
            atk INTEGER,
            stage INTEGER
        )
    """)
    conn.commit()
    conn.close()

def get_user(name):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name = ?", (name,))
    user = c.fetchone()
    conn.close()
    return user

def add_user(name, password, job, hp, atk, stage):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (name, password, job, hp, atk, stage))
    conn.commit()
    conn.close()
