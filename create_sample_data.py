import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from services.database import Database
from services.doctor_service import DoctorService
from services.patient_service import PatientService
from services.appointment_service import AppointmentService

def create_data():
    db = Database()
    db.initialize()
    doctor_service = DoctorService(db)
    patient_service = PatientService(db)
    appointment_service = AppointmentService(db)

    # Crear médicos
    print("Creando médicos...")
    doctors = [
        ("Dr. Juan Pérez", "Cardiología", "juan@clinica.com", "555-0101"),
        ("Dra. María García", "Pediatría", "maria@clinica.com", "555-0102"),
        ("Dr. Carlos López", "Dermatología", "carlos@clinica.com", "555-0103"),
        ("Dra. Ana Martínez", "Oftalmología", "ana@clinica.com", "555-0104"),
    ]
    for name, spec, email, phone in doctors:
        try:
            doctor_service.create(name, spec, email, phone)
            print(f"  ✓ {name}")
        except:
            pass

    # Crear pacientes
    print("\nCreando pacientes...")
    patients = [
        ("Juan Carlos Ruiz", "juan.ruiz@email.com", "555-0201", "12345678A"),
        ("María Elena Vásquez", "maria.vasquez@email.com", "555-0202", "87654321B"),
        ("Pedro Antonio Méndez", "pedro.mendez@email.com", "555-0203", "11223344C"),
    ]
    for name, email, phone, dni in patients:
        try:
            patient_service.create(name, email, phone, dni)
            print(f"  ✓ {name} (DNI: {dni})")
        except:
            pass

    # Crear citas de ejemplo
    print("\nCreando citas de ejemplo...")
    tomorrow = datetime.now() + timedelta(days=1)
    docs = doctor_service.get_all()
    pats = patient_service.get_all()
    if docs and pats:
        try:
            appointment_service.create(docs[0].id, pats[0].id, tomorrow.replace(hour=9, minute=0, second=0, microsecond=0))
            appointment_service.create(docs[1].id, pats[1].id, tomorrow.replace(hour=10, minute=30, second=0, microsecond=0))
            appointment_service.create(docs[2].id, pats[2].id, tomorrow.replace(hour=11, minute=0, second=0, microsecond=0))
            print("  ✓ 3 citas creadas para mañana")
        except:
            pass

    print("\n✓ Datos de ejemplo creados exitosamente")
    print("\nCredenciales de prueba:")
    print("  Pacientes: DNI 12345678A, 87654321B, 11223344C")
    print("  Admin: contraseña 'admin123'")

if __name__ == "__main__":
    create_data()
