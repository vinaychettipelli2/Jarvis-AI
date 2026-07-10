import sqlite3
import os
from datetime import datetime

DATABASE_PATH = os.path.join("data", "jarvis.db")


class Database:

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.create_tables()

    def create_tables(self):
        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE,
            value TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_message TEXT,
            jarvis_response TEXT
        )
        """)

        self.connection.commit()

    def save_memory(self, key, value):
        cursor = self.connection.cursor()

        cursor.execute("""
        INSERT OR REPLACE INTO user_memory(key, value)
        VALUES(?, ?)
        """, (key, value))

        self.connection.commit()

    def get_memory(self, key):
        cursor = self.connection.cursor()

        cursor.execute("""
        SELECT value
        FROM user_memory
        WHERE key = ?
        """, (key,))

        row = cursor.fetchone()

        if row:
            return row[0]

        return None

    def save_conversation(self, user_message, jarvis_response):
        cursor = self.connection.cursor()

        cursor.execute("""
        INSERT INTO conversations(timestamp, user_message, jarvis_response)
        VALUES(?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_message,
            jarvis_response
        ))

        self.connection.commit()