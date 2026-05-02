from datetime import datetime
from models.appointment import Appointment, AppointmentStatus


class AppointmentService:
    def __init__(self, db):
        self.db = db

    def create(self, doctor_id, patient_id, dt, notes=None):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO appointments (doctor_id, patient_id, datetime, status, notes) VALUES (?, ?, ?, ?, ?)",
                (doctor_id, patient_id, dt.isoformat(), AppointmentStatus.SCHEDULED.value, notes)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            self.db.close()

    def get_all(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, d.name as doctor_name, p.name as patient_name
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN patients p ON a.patient_id = p.id
            ORDER BY a.datetime
        """)
        rows = cursor.fetchall()
        self.db.close()
        return rows

    def get_by_patient(self, patient_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, d.name as doctor_name, p.name as patient_name
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN patients p ON a.patient_id = p.id
            WHERE a.patient_id = ? ORDER BY a.datetime
        """, (patient_id,))
        rows = cursor.fetchall()
        self.db.close()
        return rows

    def get_by_doctor(self, doctor_id, date=None):
        conn = self.db.connect()
        cursor = conn.cursor()
        if date:
            cursor.execute("""
                SELECT a.*, d.name as doctor_name, p.name as patient_name
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.id
                JOIN patients p ON a.patient_id = p.id
                WHERE a.doctor_id = ? AND date(a.datetime) = ? ORDER BY a.datetime
            """, (doctor_id, date.isoformat()))
        else:
            cursor.execute("""
                SELECT a.*, d.name as doctor_name, p.name as patient_name
                FROM appointments a
                JOIN doctors d ON a.doctor_id = d.id
                JOIN patients p ON a.patient_id = p.id
                WHERE a.doctor_id = ? ORDER BY a.datetime
            """, (doctor_id,))
        rows = cursor.fetchall()
        self.db.close()
        return rows

    def cancel(self, appointment_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE appointments SET status = ? WHERE id = ?",
            (AppointmentStatus.CANCELLED.value, appointment_id)
        )
        conn.commit()
        self.db.close()

    def is_doctor_available(self, doctor_id, dt):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM appointments WHERE doctor_id = ? AND datetime = ? AND status = ?",
            (doctor_id, dt.isoformat(), AppointmentStatus.SCHEDULED.value)
        )
        count = cursor.fetchone()[0]
        self.db.close()
        return count == 0
