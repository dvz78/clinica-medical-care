from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    username: str
    role: str
    doctor_id: Optional[int] = None
    patient_id: Optional[int] = None

    def __str__(self):
        return f"{self.username} ({self.role})"
