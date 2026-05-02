from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class AppointmentStatus(Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Appointment:
    id: Optional[int]
    doctor_id: int
    patient_id: int
    datetime: datetime
    status: AppointmentStatus
    notes: Optional[str] = None

    def __str__(self):
        return f"Cita {self.id} - {self.datetime.strftime('%Y-%m-%d %H:%M')} - {self.status.value}"
