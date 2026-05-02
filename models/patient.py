from dataclasses import dataclass
from typing import Optional


@dataclass
class Patient:
    id: Optional[int]
    name: str
    email: str
    phone: str
    dni: str

    def __str__(self):
        return f"{self.name} (DNI: {self.dni})"
