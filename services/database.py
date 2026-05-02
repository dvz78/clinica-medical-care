import sqlite3
import os
from pathlib import Path


class Database:
    def __init__(self, db_path: str = "data/clinic.db"):
        self.db_path = db_path
        Path(os.path.dirname(db_path)).mkdir(parents=True, exist_ok=True)
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()

    def initialize(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                doctor_id INTEGER,
                patient_id INTEGER,
                FOREIGN KEY (doctor_id) REFERENCES doctors(id),
                FOREIGN KEY (patient_id) REFERENCES patients(id)
            );

            CREATE TABLE IF NOT EXISTS doctors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                specialty TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                start_hour TEXT DEFAULT '08:00',
                end_hour TEXT DEFAULT '17:00'
            );

            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT NOT NULL,
                dni TEXT UNIQUE NOT NULL
            );

            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doctor_id INTEGER NOT NULL,
                patient_id INTEGER NOT NULL,
                datetime TEXT NOT NULL,
                status TEXT DEFAULT 'scheduled',
                notes TEXT,
                FOREIGN KEY (doctor_id) REFERENCES doctors(id),
                FOREIGN KEY (patient_id) REFERENCES patients(id)
            );

            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                user_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        conn.commit()
        self.close()
