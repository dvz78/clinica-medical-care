from dataclasses import dataclass
from datetime import time
from typing import Optional


@dataclass
class Doctor:
    id: Optional[int]
    name: str
    specialty: str
    email: str
    phone: str
    start_hour: time = time(8, 0)
    end_hour: time = time(17, 0)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialty}"
