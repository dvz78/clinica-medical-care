#!/usr/bin/env python3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.database import Database
from services.demo_service import DemoService


def main():
    print("=== CARGANDO DATOS DE EJEMPLO ===\n")
    db = Database()
    db.initialize()
    demo = DemoService(db)
    demo.load_demo_data()
    print("\n✓ Ejecute ahora: python3 run_gui.py")


if __name__ == "__main__":
    main()
