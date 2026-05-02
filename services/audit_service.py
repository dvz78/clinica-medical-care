from datetime import datetime


class AuditService:
    def __init__(self, db):
        self.db = db

    def log(self, user_id, action, details=None):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO audit_log (timestamp, user_id, action, details) VALUES (?, ?, ?, ?)",
                (datetime.now().isoformat(), user_id, action, details)
            )
            conn.commit()
        finally:
            self.db.close()

    def get_all(self, limit=100):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, u.username, u.role
            FROM audit_log a
            LEFT JOIN users u ON a.user_id = u.id
            ORDER BY a.timestamp DESC LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        self.db.close()
        return rows
