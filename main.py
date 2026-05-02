import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.database import Database
from services.doctor_service import DoctorService
from services.patient_service import PatientService
from services.appointment_service import AppointmentService
from ui.console import ClinicConsole


def main():
    db = Database()
    db.initialize()
    doctor_service = DoctorService(db)
    patient_service = PatientService(db)
    appointment_service = AppointmentService(db)
    console = ClinicConsole(doctor_service, patient_service, appointment_service)
    console.run()


if __name__ == "__main__":
    main()
