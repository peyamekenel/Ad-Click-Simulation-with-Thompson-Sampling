import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = sqlite3.connect('ads.db')
    try:
        yield conn
    finally:
        conn.close()

def create_table():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ad_clicks (
                ad_id INTEGER,
                user_id INTEGER,
                click_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                clicked BOOLEAN
            )
        ''')
        conn.commit()

def fetch_latest_clicks(conn, limit=500):
    cursor = conn.cursor()
    cursor.execute("SELECT ad_id, clicked FROM ad_clicks ORDER BY click_time DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    return rows

def insert_click_data(conn, ad_id, user_id, clicked):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ad_clicks (ad_id, user_id, click_time, clicked) VALUES (?, ?, CURRENT_TIMESTAMP, ?)",
        (ad_id, user_id, clicked)
    )
    conn.commit()
