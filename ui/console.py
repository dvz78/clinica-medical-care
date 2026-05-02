from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.align import Align
from rich.text import Text
from models.appointment import AppointmentStatus


class ClinicConsole:
    ADMIN_PASSWORD = "admin123"

    def __init__(self, doctor_service, patient_service, appointment_service):
        self.doctor_service = doctor_service
        self.patient_service = patient_service
        self.appointment_service = appointment_service
        self.console = Console()
        self.current_patient = None

    def run(self):
        self._show_welcome()
        while True:
            choice = self._main_menu()
            if choice == "1":
                self._patient_login()
            elif choice == "2":
                self._admin_login()
            elif choice == "0":
                self._show_goodbye()
                break

    def _show_welcome(self):
        self.console.clear()
        panel = Panel(
            Align.center(
                Text("CLÍNICA MEDICAL CARE", style="bold white on blue"),
            ),
            subtitle="[italic]Sistema de Gestión de Citas[/italic]",
            border_style="blue"
        )
        self.console.print(panel)
        self.console.print("\n[dim]Presione Enter para continuar...[/dim]")
        input()

    def _main_menu(self):
        self.console.clear()
        table = Table(title="MENÚ PRINCIPAL", show_header=False, box=None)
        table.add_column("Opción", style="cyan", width=10)
        table.add_column("Descripción", style="white")
        table.add_row("[1]", "Acceso Pacientes")
        table.add_row("[2]", "Acceso Administrador")
        table.add_row("[0]", "Salir del Sistema")
        self.console.print(table)
        return Prompt.ask("\nSeleccione una opción", choices=["1", "2", "0"], default="1")

    def _patient_login(self):
        self.console.clear()
        self.console.print(Panel("ACCESO PACIENTES", style="green"))
        dni = Prompt.ask("\nIngrese su DNI")
        patient = self.patient_service.find_by_dni(dni)
        if not patient:
            self.console.print("[red]DNI no registrado. Por favor regístrese primero.[/red]")
            if Confirm.ask("¿Desea registrarse ahora?"):
                self._register_patient()
            input("\nPresione Enter para continuar...")
            return
        self.current_patient = patient
        self.console.print(f"\n[green]¡Bienvenido/a {patient.name}![/green]")
        input("Presione Enter para continuar...")
        self._patient_menu()

    def _admin_login(self):
        self.console.clear()
        self.console.print(Panel("ACCESO ADMINISTRADOR", style="red"))
        password = Prompt.ask("\nIngrese contraseña", password=True)
        if password != self.ADMIN_PASSWORD:
            self.console.print("[red]Contraseña incorrecta[/red]")
            input("Presione Enter para continuar...")
            return
        self.console.print("\n[green]Acceso concedido[/green]")
        input("Presione Enter para continuar...")
        self._admin_menu()

    def _patient_menu(self):
        while True:
            self.console.clear()
            self.console.print(Panel(f"MENÚ PACIENTE - {self.current_patient.name}", style="green"))
            table = Table(show_header=False, box=None)
            table.add_column("Opción", style="cyan", width=10)
            table.add_column("Descripción", style="white")
            table.add_row("[1]", "Reservar Cita")
            table.add_row("[2]", "Cancelar Cita")
            table.add_row("[3]", "Mis Citas")
            table.add_row("[4]", "Datos Personales")
            table.add_row("[0]", "Cerrar Sesión")
            self.console.print(table)
            choice = Prompt.ask("\nSeleccione una opción", choices=["1", "2", "3", "4", "0"], default="0")
            if choice == "1":
                self._book_appointment()
            elif choice == "2":
                self._cancel_appointment()
            elif choice == "3":
                self._view_my_appointments()
            elif choice == "4":
                self._show_patient_data()
            elif choice == "0":
                self.current_patient = None
                break

    def _admin_menu(self):
        while True:
            self.console.clear()
            self.console.print(Panel("MENÚ ADMINISTRADOR", style="red"))
            table = Table(show_header=False, box=None)
            table.add_column("Opción", style="cyan", width=10)
            table.add_column("Descripción", style="white")
            table.add_row("[1]", "Registrar Médico")
            table.add_row("[2]", "Lista de Médicos")
            table.add_row("[3]", "Lista de Pacientes")
            table.add_row("[4]", "Todas las Citas")
            table.add_row("[5]", "Citas por Médico")
            table.add_row("[6]", "Citas por Paciente")
            table.add_row("[7]", "Registrar Paciente")
            table.add_row("[0]", "Cerrar Sesión")
            self.console.print(table)
            choice = Prompt.ask("\nSeleccione una opción", choices=["1", "2", "3", "4", "5", "6", "7", "0"], default="0")
            if choice == "1":
                self._register_doctor()
            elif choice == "2":
                self._list_doctors()
            elif choice == "3":
                self._list_patients()
            elif choice == "4":
                self._list_appointments()
            elif choice == "5":
                self._view_doctor_appointments_admin()
            elif choice == "6":
                self._view_patient_appointments_admin()
            elif choice == "7":
                self._register_patient()
            elif choice == "0":
                break

    def _register_patient(self):
        self.console.clear()
        self.console.print(Panel("REGISTRO DE PACIENTE", style="green"))
        name = Prompt.ask("Nombre completo")
        email = Prompt.ask("Email")
        phone = Prompt.ask("Teléfono")
        dni = Prompt.ask("DNI")
        try:
            patient_id = self.patient_service.create(name, email, phone, dni)
            self.console.print(f"\n[green]✓ Paciente registrado exitosamente[/green]")
            self.console.print(f"[green]ID de Paciente: {patient_id}[/green]")
        except Exception as e:
            self.console.print(f"\n[red]Error: {e}[/red]")
        input("\nPresione Enter para continuar...")

    def _register_doctor(self):
        self.console.clear()
        self.console.print(Panel("REGISTRO DE MÉDICO", style="red"))
        name = Prompt.ask("Nombre completo")
        specialty = Prompt.ask("Especialidad")
        email = Prompt.ask("Email")
        phone = Prompt.ask("Teléfono")
        start = Prompt.ask("Hora inicio (HH:MM)", default="08:00")
        end = Prompt.ask("Hora fin (HH:MM)", default="17:00")
        try:
            doctor_id = self.doctor_service.create(name, specialty, email, phone, start, end)
            self.console.print(f"\n[green]✓ Médico registrado exitosamente[/green]")
            self.console.print(f"[green]ID de Médico: {doctor_id}[/green]")
        except Exception as e:
            self.console.print(f"\n[red]Error: {e}[/red]")
        input("\nPresione Enter para continuar...")

    def _book_appointment(self):
        self.console.clear()
        self.console.print(Panel("RESERVAR CITA", style="green"))
        doctors = self.doctor_service.get_all()
        if not doctors:
            self.console.print("[yellow]No hay médicos registrados[/yellow]")
            input("Presione Enter para continuar...")
            return
        table = Table(title="Médicos Disponibles")
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="green")
        table.add_column("Especialidad", style="yellow")
        for doc in doctors:
            table.add_row(str(doc.id), doc.name, doc.specialty)
        self.console.print(table)
        doctor_id = int(Prompt.ask("\nID del médico"))
        date_str = Prompt.ask("Fecha (YYYY-MM-DD)")
        time_str = Prompt.ask("Hora (HH:MM)")
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            if not self.appointment_service.is_doctor_available(doctor_id, dt):
                self.console.print("\n[red]El médico ya tiene una cita a esa hora[/red]")
                input("Presione Enter para continuar...")
                return
            notes = Prompt.ask("Notas (opcional)", default="")
            appt_id = self.appointment_service.create(doctor_id, self.current_patient.id, dt, notes or None)
            self.console.print(f"\n[green]✓ Cita reservada exitosamente[/green]")
            self.console.print(f"[green]Número de Cita: {appt_id}[/green]")
            self.console.print(f"[green]Fecha y Hora: {date_str} {time_str}[/green]")
        except Exception as e:
            self.console.print(f"\n[red]Error: {e}[/red]")
        input("\nPresione Enter para continuar...")

    def _cancel_appointment(self):
        self.console.clear()
        self.console.print(Panel("CANCELAR CITA", style="green"))
        appointments = self.appointment_service.get_by_patient(self.current_patient.id)
        scheduled = [a for a in appointments if a['status'] == AppointmentStatus.SCHEDULED.value]
        if not scheduled:
            self.console.print("[yellow]No tienes citas programadas[/yellow]")
            input("Presione Enter para continuar...")
            return
        table = Table(title="Citas Programadas")
        table.add_column("ID", style="cyan")
        table.add_column("Fecha", style="green")
        table.add_column("Médico", style="yellow")
        for row in scheduled:
            table.add_row(str(row['id']), row['datetime'], row['doctor_name'])
        self.console.print(table)
        appt_id = int(Prompt.ask("\nID de la cita a cancelar"))
        if Confirm.ask("¿Está seguro de cancelar esta cita?"):
            self.appointment_service.cancel(appt_id)
            self.console.print("\n[green]✓ Cita cancelada exitosamente[/green]")
        else:
            self.console.print("\n[yellow]Cancelación abortada[/yellow]")
        input("Presione Enter para continuar...")

    def _view_my_appointments(self):
        self.console.clear()
        self.console.print(Panel(f"MIS CITAS - {self.current_patient.name}", style="green"))
        appointments = self.appointment_service.get_by_patient(self.current_patient.id)
        self._display_appointments(appointments)
        input("\nPresione Enter para continuar...")

    def _show_patient_data(self):
        self.console.clear()
        self.console.print(Panel("DATOS PERSONALES", style="green"))
        p = self.current_patient
        table = Table(show_header=False, box=None)
        table.add_row("Nombre:", p.name)
        table.add_row("DNI:", p.dni)
        table.add_row("Email:", p.email)
        table.add_row("Teléfono:", p.phone)
        self.console.print(table)
        input("\nPresione Enter para continuar...")

    def _list_doctors(self):
        self.console.clear()
        self.console.print(Panel("LISTA DE MÉDICOS", style="red"))
        doctors = self.doctor_service.get_all()
        table = Table()
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="green")
        table.add_column("Especialidad", style="yellow")
        table.add_column("Email", style="blue")
        table.add_column("Teléfono", style="magenta")
        for doc in doctors:
            table.add_row(str(doc.id), doc.name, doc.specialty, doc.email, doc.phone)
        self.console.print(table)
        input("\nPresione Enter para continuar...")

    def _list_patients(self):
        self.console.clear()
        self.console.print(Panel("LISTA DE PACIENTES", style="red"))
        patients = self.patient_service.get_all()
        table = Table()
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="green")
        table.add_column("DNI", style="yellow")
        table.add_column("Email", style="blue")
        table.add_column("Teléfono", style="magenta")
        for p in patients:
            table.add_row(str(p.id), p.name, p.dni, p.email, p.phone)
        self.console.print(table)
        input("\nPresione Enter para continuar...")

    def _list_appointments(self):
        self.console.clear()
        self.console.print(Panel("TODAS LAS CITAS", style="red"))
        appointments = self.appointment_service.get_all()
        self._display_appointments(appointments)
        input("\nPresione Enter para continuar...")

    def _view_doctor_appointments_admin(self):
        self.console.clear()
        doctors = self.doctor_service.get_all()
        table = Table(title="Médicos")
        table.add_column("ID", style="cyan")
        table.add_column("Nombre", style="green")
        table.add_column("Especialidad", style="yellow")
        for doc in doctors:
            table.add_row(str(doc.id), doc.name, doc.specialty)
        self.console.print(table)
        doctor_id = int(Prompt.ask("\nID del médico"))
        appointments = self.appointment_service.get_by_doctor(doctor_id)
        self._display_appointments(appointments)
        input("\nPresione Enter para continuar...")

    def _view_patient_appointments_admin(self):
        dni = Prompt.ask("DNI del paciente")
        patient = self.patient_service.find_by_dni(dni)
        if not patient:
            self.console.print("[red]Paciente no encontrado[/red]")
            input("Presione Enter para continuar...")
            return
        appointments = self.appointment_service.get_by_patient(patient.id)
        self._display_appointments(appointments)
        input("\nPresione Enter para continuar...")

    def _display_appointments(self, appointments):
        if not appointments:
            self.console.print("[yellow]No hay citas para mostrar[/yellow]")
            return
        table = Table()
        table.add_column("ID", style="cyan")
        table.add_column("Fecha", style="green")
        table.add_column("Médico", style="yellow")
        table.add_column("Paciente", style="magenta")
        table.add_column("Estado", style="blue")
        for row in appointments:
            table.add_row(str(row['id']), row['datetime'], row['doctor_name'], row['patient_name'], row['status'])
        self.console.print(table)

    def _show_goodbye(self):
        self.console.clear()
        self.console.print(Panel(
            Align.center(Text("¡Gracias por usar CLÍNICA MEDICAL CARE!", style="bold white on blue")),
            border_style="blue"
        ))
