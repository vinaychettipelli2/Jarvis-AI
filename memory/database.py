import sqlite3
import os
from datetime import datetime


class Database:

    def __init__(self):

        os.makedirs("data", exist_ok=True)

        self.database_path = os.path.join(
            "data",
            "jarvis.db"
        )

        self.connection = sqlite3.connect(
            self.database_path,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.create_tables()

    # =====================================================
    # CREATE TABLES
    # =====================================================

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS user_memory(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            memory_key TEXT UNIQUE,

            memory_value TEXT,

            category TEXT,

            created_at TEXT,

            updated_at TEXT

        )

        """)

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS conversations(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_message TEXT,

            assistant_message TEXT,

            created_at TEXT

        )

        """)

        self.connection.commit()

    # =====================================================
    # SAVE MEMORY
    # =====================================================

    def save_memory(
        self,
        key,
        value,
        category="general"
    ):

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor = self.connection.cursor()

        cursor.execute("""

        INSERT INTO user_memory(

            memory_key,

            memory_value,

            category,

            created_at,

            updated_at

        )

        VALUES(?,?,?,?,?)

        ON CONFLICT(memory_key)

        DO UPDATE SET

            memory_value=excluded.memory_value,

            category=excluded.category,

            updated_at=excluded.updated_at

        """,

        (

            key,

            value,

            category,

            now,

            now

        )

        )

        self.connection.commit()

    # =====================================================
    # GET MEMORY
    # =====================================================

    def get_memory(self, key):

        cursor = self.connection.cursor()

        cursor.execute("""

        SELECT *

        FROM user_memory

        WHERE memory_key=?

        """,

        (key,)

        )

        row = cursor.fetchone()

        if row:

            return dict(row)

        return None

    # =====================================================
    # DELETE MEMORY
    # =====================================================

    def delete_memory(self, key):

        cursor = self.connection.cursor()

        cursor.execute("""

        DELETE

        FROM user_memory

        WHERE memory_key=?

        """,

        (key,)

        )

        self.connection.commit()

    # =====================================================
    # LIST MEMORIES
    # =====================================================

    def list_memories(self):

        cursor = self.connection.cursor()

        cursor.execute("""

        SELECT *

        FROM user_memory

        ORDER BY memory_key

        """)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    # =====================================================
    # SEARCH MEMORY
    # =====================================================

    def search_memory(self, keyword):

        cursor = self.connection.cursor()

        cursor.execute("""

        SELECT *

        FROM user_memory

        WHERE

        memory_key LIKE ?

        OR

        memory_value LIKE ?

        """,

        (

            f"%{keyword}%",

            f"%{keyword}%"

        )

        )

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    # =====================================================
    # MEMORY COUNT
    # =====================================================

    def memory_count(self):

        cursor = self.connection.cursor()

        cursor.execute("""

        SELECT COUNT(*)

        FROM user_memory

        """)

        return cursor.fetchone()[0]

    # =====================================================
    # SAVE CHAT
    # =====================================================

    def save_chat(
        self,
        user_message,
        assistant_message
    ):

        cursor = self.connection.cursor()

        cursor.execute("""

        INSERT INTO conversations(

            user_message,

            assistant_message,

            created_at

        )

        VALUES(?,?,?)

        """,

        (

            user_message,

            assistant_message,

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        )

        )

        self.connection.commit()

    # =====================================================
    # RECENT CHAT
    # =====================================================

    def recent_chat(self, limit=10):

        cursor = self.connection.cursor()

        cursor.execute("""

        SELECT *

        FROM conversations

        ORDER BY id DESC

        LIMIT ?

        """,

        (limit,)

        )

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        self.connection.close()