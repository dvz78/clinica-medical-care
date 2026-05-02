from datetime import datetime, timedelta
from collections import Counter


class ReportService:
    def __init__(self, db):
        self.db = db

    def appointments_by_doctor(self, days=30):
        conn = self.db.connect()
        cursor = conn.cursor()
        since = (datetime.now() - timedelta(days=days)).isoformat()
        cursor.execute("""
            SELECT d.name, COUNT(*) as count
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.datetime >= ? AND a.status = 'scheduled'
            GROUP BY d.id, d.name
            ORDER BY count DESC
        """, (since,))
        rows = cursor.fetchall()
        self.db.close()
        return [(row['name'], row['count']) for row in rows]

    def appointments_by_specialty(self, days=30):
        conn = self.db.connect()
        cursor = conn.cursor()
        since = (datetime.now() - timedelta(days=days)).isoformat()
        cursor.execute("""
            SELECT d.specialty, COUNT(*) as count
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            WHERE a.datetime >= ? AND a.status = 'scheduled'
            GROUP BY d.specialty
            ORDER BY count DESC
        """, (since,))
        rows = cursor.fetchall()
        self.db.close()
        return [(row['specialty'], row['count']) for row in rows]

    def daily_appointments(self, date=None):
        if not date:
            date = datetime.now().date().isoformat()
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM appointments
            WHERE date(datetime) = ? AND status = 'scheduled'
        """, (date,))
        row = cursor.fetchone()
        self.db.close()
        return row['count'] if row else 0

    def cancellation_rate(self, days=30):
        conn = self.db.connect()
        cursor = conn.cursor()
        since = (datetime.now() - timedelta(days=days)).isoformat()
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM appointments
            WHERE datetime >= ?
            GROUP BY status
        """, (since,))
        rows = cursor.fetchall()
        self.db.close()
        total = sum(row['count'] for row in rows)
        cancelled = next((row['count'] for row in rows if row['status'] == 'cancelled'), 0)
        return (cancelled / total * 100) if total > 0 else 0
