import hashlib
from models.user import User


class UserService:
    def __init__(self, db):
        self.db = db

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create(self, username, password, role, doctor_id=None, patient_id=None):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role, doctor_id, patient_id) VALUES (?, ?, ?, ?, ?)",
                (username, self._hash_password(password), role, doctor_id, patient_id)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            self.db.close()

    def authenticate(self, username, password):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                       (username, self._hash_password(password)))
        row = cursor.fetchone()
        self.db.close()
        if row:
            return User(
                id=row['id'], username=row['username'], role=row['role'],
                doctor_id=row['doctor_id'], patient_id=row['patient_id']
            )
        return None

    def get_by_id(self, user_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        self.db.close()
        if row:
            return User(
                id=row['id'], username=row['username'], role=row['role'],
                doctor_id=row['doctor_id'], patient_id=row['patient_id']
            )
        return None

    def create_default_admin(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ('admin', self._hash_password('admin123'), 'admin')
            )
            conn.commit()
        self.db.close()
