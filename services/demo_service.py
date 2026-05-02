from datetime import datetime, timedelta
from services.doctor_service import DoctorService
from services.patient_service import PatientService
from services.appointment_service import AppointmentService
from services.user_service import UserService


class DemoService:
    def __init__(self, db):
        self.db = db
        self.doctor_service = DoctorService(db)
        self.patient_service = PatientService(db)
        self.appointment_service = AppointmentService(db)
        self.user_service = UserService(db)

    def load_demo_data(self):
        """Carga los ejemplos mostrados en el README"""
        # Limpiar datos existentes (opcional)
        
        # 1. Crear médicos (Ejemplo 3)
        doctors_data = [
            ("Dr. Juan Pérez", "Cardiología", "juan@clinica.com", "555-0101"),
            ("Dra. María García", "Pediatría", "maria@clinica.com", "555-0102"),
            ("Dr. Carlos López", "Dermatología", "carlos@clinica.com", "555-0103"),
            ("Dra. Ana Martínez", "Oftalmología", "ana@clinica.com", "555-0104"),
        ]
        doctor_ids = {}
        for name, spec, email, phone in doctors_data:
            try:
                doc_id = self.doctor_service.create(name, spec, email, phone)
                doctor_ids[name] = doc_id
                print(f"  ✓ {name} (ID: {doc_id})")
            except:
                # Si ya existe, obtener ID
                doctors = self.doctor_service.get_all()
                for d in doctors:
                    if d.name == name:
                        doctor_ids[name] = d.id

        # 2. Crear pacientes (Ejemplo 1, 4)
        patients_data = [
            ("Juan Carlos Ruiz", "juan.ruiz@email.com", "555-0201", "12345678A"),
            ("María Elena Vásquez", "maria.vasquez@email.com", "555-0202", "87654321B"),
            ("Pedro Antonio Méndez", "pedro.mendez@email.com", "555-0203", "11223344C"),
        ]
        patient_ids = {}
        for name, email, phone, dni in patients_data:
            try:
                pat_id = self.patient_service.create(name, email, phone, dni)
                patient_ids[dni] = pat_id
                print(f"  ✓ {name} (DNI: {dni})")
            except:
                patients = self.patient_service.get_all()
                for p in patients:
                    if p.dni == dni:
                        patient_ids[dni] = p.id

        # 3. Crear usuarios con roles
        users_data = [
            ("admin", "admin123", "admin", None, None),
            ("juan_perez", "doctor123", "doctor", doctor_ids.get("Dr. Juan Pérez"), None),
            ("maria_garcia", "doctor123", "doctor", doctor_ids.get("Dra. María García"), None),
            ("paciente1", "paciente123", "patient", None, patient_ids.get("12345678A")),
            ("paciente2", "paciente123", "patient", None, patient_ids.get("87654321B")),
        ]
        for username, password, role, doctor_id, patient_id in users_data:
            try:
                self.user_service.create(username, password, role, doctor_id, patient_id)
                print(f"  ✓ Usuario: {username} ({role})")
            except:
                pass

        # 4. Crear citas de ejemplo (Ejemplo 3, 4, 5)
        tomorrow = datetime.now() + timedelta(days=1)
        try:
            # Cita 1: Juan Pérez (médico) con Juan Carlos Ruiz (paciente) - 09:00
            if doctor_ids.get("Dr. Juan Pérez") and patient_ids.get("12345678A"):
                self.appointment_service.create(
                    doctor_ids["Dr. Juan Pérez"],
                    patient_ids["12345678A"],
                    tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
                )
                print(f"  ✓ Cita #1: Dr. Juan Pérez - 09:00")

            # Cita 2: María García con María Elena Vásquez - 10:30
            if doctor_ids.get("Dra. María García") and patient_ids.get("87654321B"):
                self.appointment_service.create(
                    doctor_ids["Dra. María García"],
                    patient_ids["87654321B"],
                    tomorrow.replace(hour=10, minute=30, second=0, microsecond=0)
                )
                print(f"  ✓ Cita #2: Dra. María García - 10:30")

            # Cita 3: Carlos López con Pedro Antonio Méndez - 11:00 (cancelada)
            if doctor_ids.get("Dr. Carlos López") and patient_ids.get("11223344C"):
                appt_id = self.appointment_service.create(
                    doctor_ids["Dr. Carlos López"],
                    patient_ids["11223344C"],
                    tomorrow.replace(hour=11, minute=0, second=0, microsecond=0)
                )
                self.appointment_service.cancel(appt_id)
                print(f"  ✓ Cita #3: Dr. Carlos López - 11:00 (CANCELADA)")
        except Exception as e:
            print(f"  Error creando citas: {e}")

        print("\n✓ Datos de ejemplo cargados exitosamente")
        print("\n=== CREDENCIALES PARA PROBAR ===")
        print("Admin: admin / admin123")
        print("Médico: juan_perez / doctor123")
        print("Paciente (DNI): 12345678A, 87654321B")
        print("===================================")

        return {
            "doctors": len(doctor_ids),
            "patients": len(patient_ids),
            "users": len(users_data)
        }
