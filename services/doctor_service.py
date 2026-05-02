from datetime import time
from models.doctor import Doctor


class DoctorService:
    def __init__(self, db):
        self.db = db

    def create(self, name, specialty, email, phone, start_hour=None, end_hour=None):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO doctors (name, specialty, email, phone, start_hour, end_hour) VALUES (?, ?, ?, ?, ?, ?)",
                (name, specialty, email, phone,
                 start_hour or '08:00',
                 end_hour or '17:00')
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            self.db.close()

    def get_all(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors ORDER BY name")
        rows = cursor.fetchall()
        self.db.close()
        return [Doctor(
            id=row['id'], name=row['name'], specialty=row['specialty'],
            email=row['email'], phone=row['phone'],
            start_hour=time.fromisoformat(row['start_hour']),
            end_hour=time.fromisoformat(row['end_hour'])
        ) for row in rows]

    def get_by_id(self, doctor_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        row = cursor.fetchone()
        self.db.close()
        if row:
            return Doctor(
                id=row['id'], name=row['name'], specialty=row['specialty'],
                email=row['email'], phone=row['phone'],
                start_hour=time.fromisoformat(row['start_hour']),
                end_hour=time.fromisoformat(row['end_hour'])
            )
        return None

    def delete(self, doctor_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
        conn.commit()
        self.db.close()
