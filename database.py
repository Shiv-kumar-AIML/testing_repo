#!/usr/bin/env python3
"""Database utilities for chatbot persistence using SQLite."""

import sqlite3
from pathlib import Path
from typing import List, Tuple


class ChatDatabase:
    def __init__(self, db_path: str = "chatbot.db"):
        self.db_path = Path(db_path)
        self.init_db()

    def init_db(self) -> None:
        """Initialize the database with tables for chat history."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    thread_id TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER,
                    role TEXT NOT NULL,  -- 'user' or 'assistant'
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                )
            """)
            conn.commit()

    def save_message(self, thread_id: str, role: str, content: str) -> None:
        """Save a message to the database."""
        with sqlite3.connect(self.db_path) as conn:
            # Get or create conversation
            cursor = conn.execute(
                "SELECT id FROM conversations WHERE thread_id = ?",
                (thread_id,)
            )
            conv = cursor.fetchone()
            if not conv:
                conn.execute(
                    "INSERT INTO conversations (thread_id) VALUES (?)",
                    (thread_id,)
                )
                conv_id = cursor.lastrowid
            else:
                conv_id = conv[0]

            # Save message
            conn.execute(
                "INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                (conv_id, role, content)
            )
            conn.commit()

    def load_messages(self, thread_id: str) -> List[Tuple[str, str]]:
        """Load messages for a thread as (role, content) tuples."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT role, content FROM messages
                WHERE conversation_id = (
                    SELECT id FROM conversations WHERE thread_id = ?
                )
                ORDER BY timestamp
            """, (thread_id,))
            return cursor.fetchall()

    def execute_query(self, query: str, params: tuple = ()) -> List[Tuple]:
        """Execute a read-only SQL query on the database, or safe DELETE on messages."""
        query_upper = query.strip().upper()
        if query_upper.startswith("SELECT"):
            pass  # Allow
        elif query_upper.startswith("DELETE FROM messages"):
            pass  # Allow safe delete
        else:
            raise ValueError("Only SELECT or DELETE FROM messages queries are allowed for security.")

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)
            if query_upper.startswith("SELECT"):
                return cursor.fetchall()
            else:
                conn.commit()
                return []  # For DELETE, return empty


# Global instance
db = ChatDatabase()
