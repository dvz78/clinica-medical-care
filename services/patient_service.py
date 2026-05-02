from models.patient import Patient


class PatientService:
    def __init__(self, db):
        self.db = db

    def create(self, name, email, phone, dni):
        conn = self.db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO patients (name, email, phone, dni) VALUES (?, ?, ?, ?)",
                (name, email, phone, dni)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            self.db.close()

    def get_all(self):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients ORDER BY name")
        rows = cursor.fetchall()
        self.db.close()
        return [Patient(
            id=row['id'], name=row['name'], email=row['email'],
            phone=row['phone'], dni=row['dni']
        ) for row in rows]

    def get_by_id(self, patient_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        row = cursor.fetchone()
        self.db.close()
        if row:
            return Patient(
                id=row['id'], name=row['name'], email=row['email'],
                phone=row['phone'], dni=row['dni']
            )
        return None

    def find_by_dni(self, dni):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE dni = ?", (dni,))
        row = cursor.fetchone()
        self.db.close()
        if row:
            return Patient(
                id=row['id'], name=row['name'], email=row['email'],
                phone=row['phone'], dni=row['dni']
            )
        return None
