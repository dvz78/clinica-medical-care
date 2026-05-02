import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.database import Database
from services.doctor_service import DoctorService
from services.patient_service import PatientService
from services.appointment_service import AppointmentService
from services.user_service import UserService
from services.audit_service import AuditService
from services.report_service import ReportService
from services.notification_service import NotificationService
from models.appointment import AppointmentStatus


class ClinicGUI:
    def __init__(self):
        self.db = Database()
        self.db.initialize()
        self.doctor_service = DoctorService(self.db)
        self.patient_service = PatientService(self.db)
        self.appointment_service = AppointmentService(self.db)
        self.user_service = UserService(self.db)
        self.audit_service = AuditService(self.db)
        self.report_service = ReportService(self.db)
        self.notification_service = NotificationService()
        self.current_user = None
        self.current_patient = None

        self.user_service.create_default_admin()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Clínica Medical Care - Sistema de Gestión")
        self.root.geometry("1000x700")
        self.root.minsize(900, 650)

        self.show_login()

    def run(self):
        self.root.mainloop()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        self.current_user = None
        self.current_patient = None

        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(expand=True, fill="both")

        left_panel = ctk.CTkFrame(main_frame, width=400, fg_color=("#1f538d", "#1f538d"))
        left_panel.pack(side="left", fill="y")
        left_panel.pack_propagate(False)

        ctk.CTkLabel(left_panel, text="CLÍNICA\nMEDICAL CARE",
                      font=ctk.CTkFont(size=32, weight="bold"),
                      text_color="white").pack(expand=True)

        right_panel = ctk.CTkFrame(main_frame, fg_color=("gray95", "gray10"))
        right_panel.pack(side="right", expand=True, fill="both")

        login_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        login_frame.pack(expand=True)

        ctk.CTkLabel(login_frame, text="INICIAR SESIÓN",
                      font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)

        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text="Usuario",
                                            width=300, height=40,
                                            font=ctk.CTkFont(size=14))
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Contraseña",
                                             width=300, height=40, show="*",
                                             font=ctk.CTkFont(size=14))
        self.password_entry.pack(pady=10)

        ctk.CTkButton(login_frame, text="INGRESAR",
                       font=ctk.CTkFont(size=14, weight="bold"),
                       width=300, height=45,
                       command=self.login).pack(pady=20)

        ctk.CTkButton(login_frame, text="SALIR",
                       font=ctk.CTkFont(size=12),
                       width=300, height=35,
                       fg_color="gray",
                       command=self.root.quit).pack()

        self.username_entry.focus()
        self.root.bind("<Return>", lambda e: self.login())

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = self.user_service.authenticate(username, password)
        if user:
            self.current_user = user
            self.audit_service.log(user.id, "login", f"Login exitoso para {username}")
            if user.role == "patient" and user.patient_id:
                self.current_patient = self.patient_service.get_by_id(user.patient_id)
                self.show_patient_menu()
            elif user.role == "doctor" and user.doctor_id:
                self.current_doctor = self.doctor_service.get_by_id(user.doctor_id)
                self.show_doctor_menu()
            else:
                self.show_admin_menu()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def show_patient_menu(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#1f538d", "#1f538d"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=f"BIENVENIDO/A {self.current_patient.name.upper()}",
                      font=ctk.CTkFont(size=18, weight="bold"),
                      text_color="white").pack(pady=25)

        content = ctk.CTkFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=60, pady=30)

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=10)

        buttons = [
            ("RESERVAR CITA", self.show_book_appointment, "#337ab7"),
            ("CANCELAR CITA", self.show_cancel_appointment, "#d9534f"),
            ("MIS CITAS", self.show_my_appointments, "#5bc0de"),
            ("MIS DATOS", self.show_patient_data, "#5cb85c"),
        ]

        for text, cmd, color in buttons:
            ctk.CTkButton(btn_frame, text=text,
                           font=ctk.CTkFont(size=14, weight="bold"),
                           width=250, height=50,
                           fg_color=color,
                           command=cmd).pack(pady=8)

        ctk.CTkButton(content, text="CERRAR SESIÓN",
                       font=ctk.CTkFont(size=12),
                       width=150, height=35,
                       fg_color="gray",
                       command=self.logout).pack(pady=20)

    def show_doctor_menu(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#5cb85c", "#5cb85c"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=f"MÉDICO: {self.current_doctor.name.upper()}",
                      font=ctk.CTkFont(size=18, weight="bold"),
                      text_color="white").pack(pady=25)

        content = ctk.CTkFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=60, pady=30)

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="MIS CITAS DE HOY",
                       font=ctk.CTkFont(size=14, weight="bold"),
                       width=250, height=50,
                       command=self.show_doctor_today).pack(pady=8)

        ctk.CTkButton(btn_frame, text="TODAS MIS CITAS",
                       font=ctk.CTkFont(size=14, weight="bold"),
                       width=250, height=50,
                       fg_color="#5bc0de",
                       command=self.show_doctor_all).pack(pady=8)

        ctk.CTkButton(content, text="CERRAR SESIÓN",
                       font=ctk.CTkFont(size=12),
                       width=150, height=35,
                       fg_color="gray",
                       command=self.logout).pack(pady=20)

    def show_admin_menu(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#d9534f", "#d9534f"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="PANEL DE ADMINISTRADOR",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(content, text="GESTIÓN DE USUARIOS",
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10, anchor="w")

        btn_frame1 = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame1.pack(fill="x", pady=5)

        buttons_row1 = [
            ("Registrar Médico", self.show_register_doctor, "#5cb85c"),
            ("Registrar Paciente", self.show_register_patient, "#5cb85c"),
            ("Nuevo Usuario", self.show_register_user, "#337ab7"),
        ]

        for text, cmd, color in buttons_row1:
            ctk.CTkButton(btn_frame1, text=text,
                           font=ctk.CTkFont(size=12, weight="bold"),
                           width=180, height=40,
                           fg_color=color,
                           command=cmd).pack(side="left", padx=5)

        ctk.CTkLabel(content, text="CONSULTAS",
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10), anchor="w")

        btn_frame2 = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame2.pack(fill="x", pady=5)

        buttons_row2 = [
            ("Lista Médicos", self.show_list_doctors, "#337ab7"),
            ("Lista Pacientes", self.show_list_patients, "#337ab7"),
            ("Todas las Citas", self.show_all_appointments, "#337ab7"),
        ]

        for text, cmd, color in buttons_row2:
            ctk.CTkButton(btn_frame2, text=text,
                           font=ctk.CTkFont(size=12, weight="bold"),
                           width=180, height=40,
                           fg_color=color,
                           command=cmd).pack(side="left", padx=5)

        ctk.CTkLabel(content, text="REPORTES Y AUDITORÍA",
                      font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10), anchor="w")

        btn_frame3 = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame3.pack(fill="x", pady=5)

        buttons_row3 = [
            ("Ver Reportes", self.show_reports, "#f0ad4e"),
            ("Log de Auditoría", self.show_audit_log, "#f0ad4e"),
        ]

        for text, cmd, color in buttons_row3:
            ctk.CTkButton(btn_frame3, text=text,
                           font=ctk.CTkFont(size=12, weight="bold"),
                           width=180, height=40,
                           fg_color=color,
                           command=cmd).pack(side="left", padx=5)

        ctk.CTkButton(content, text="CERRAR SESIÓN",
                       font=ctk.CTkFont(size=12),
                       width=150, height=35,
                       fg_color="gray",
                       command=self.logout).pack(pady=20)

    def show_register_user(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#337ab7", "#337ab7"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="REGISTRAR USUARIO",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=60, pady=20)

        self.user_entries = {}
        ctk.CTkLabel(content, text="Usuario:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5), anchor="w")
        self.user_entries['username'] = ctk.CTkEntry(content, width=350, height=38)
        self.user_entries['username'].pack(pady=5)

        ctk.CTkLabel(content, text="Contraseña:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5), anchor="w")
        self.user_entries['password'] = ctk.CTkEntry(content, width=350, height=38, show="*")
        self.user_entries['password'].pack(pady=5)

        ctk.CTkLabel(content, text="Rol:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5), anchor="w")
        self.user_role = ctk.StringVar(value="patient")
        roles_frame = ctk.CTkFrame(content, fg_color="transparent")
        roles_frame.pack(fill="x", pady=5)
        for role in ["patient", "doctor", "admin"]:
            ctk.CTkRadioButton(roles_frame, text=role.capitalize(),
                                variable=self.user_role, value=role).pack(side="left", padx=10)

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="REGISTRAR",
                       font=ctk.CTkFont(size=14, weight="bold"),
                       width=150, height=45,
                       command=self.register_user).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_admin_menu).pack(side="left", padx=10)

    def register_user(self):
        try:
            username = self.user_entries['username'].get()
            password = self.user_entries['password'].get()
            role = self.user_role.get()
            if not username or not password:
                messagebox.showerror("Error", "Complete todos los campos")
                return
            user_id = self.user_service.create(username, password, role)
            self.audit_service.log(self.current_user.id, "create_user",
                                    f"Usuario {username} creado con rol {role}")
            messagebox.showinfo("Éxito", f"Usuario registrado. ID: {user_id}")
            self.show_admin_menu()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_reports(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#f0ad4e", "#f0ad4e"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="REPORTES Y ESTADÍSTICAS",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=40, pady=20)

        ctk.CTkLabel(content, text="Citas por Médico (últimos 30 días):",
                      font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10, anchor="w")
        for name, count in self.report_service.appointments_by_doctor():
            frame = ctk.CTkFrame(content, fg_color=("#2b2b2b", "#2b2b2b"))
            frame.pack(fill="x", pady=2, padx=10)
            ctk.CTkLabel(frame, text=f"{name}: {count} citas",
                          font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(content, text="\nCitas por Especialidad (últimos 30 días):",
                      font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10, anchor="w")
        for spec, count in self.report_service.appointments_by_specialty():
            frame = ctk.CTkFrame(content, fg_color=("#2b2b2b", "#2b2b2b"))
            frame.pack(fill="x", pady=2, padx=10)
            ctk.CTkLabel(frame, text=f"{spec}: {count} citas",
                          font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=5)

        rate = self.report_service.cancellation_rate()
        ctk.CTkLabel(content, text=f"\nTasa de cancelación (30 días): {rate:.1f}%",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      text_color="#e74c3c").pack(pady=10, anchor="w")

        daily = self.report_service.daily_appointments()
        ctk.CTkLabel(content, text=f"Citas hoy: {daily}",
                      font=ctk.CTkFont(size=14, weight="bold"),
                      text_color="#2ecc71").pack(pady=5, anchor="w")

        ctk.CTkButton(content, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_admin_menu).pack(pady=20)

    def show_audit_log(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#f0ad4e", "#f0ad4e"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="LOG DE AUDITORÍA",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=20, pady=20)

        logs = self.audit_service.get_all(50)
        for row in logs:
            frame = ctk.CTkFrame(content, fg_color=("#2b2b2b", "#2b2b2b"))
            frame.pack(fill="x", pady=3, padx=10)
            user_str = row['username'] or 'Sistema'
            ctk.CTkLabel(frame, text=f"{row['timestamp'][:19]} - {user_str} ({row['role'] or 'N/A'})",
                          font=ctk.CTkFont(size=11, weight="bold"),
                          text_color="#5bc0de").pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(frame, text=row['action'] + (f" - {row['details']}" if row['details'] else ""),
                          font=ctk.CTkFont(size=11)).pack(anchor="w", padx=10, pady=(0, 5))

        ctk.CTkButton(content, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_admin_menu).pack(pady=20)

    def show_book_appointment(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#1f538d", "#1f538d"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="RESERVAR CITA",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=40, pady=20)

        doctors = self.doctor_service.get_all()
        if not doctors:
            ctk.CTkLabel(content, text="No hay médicos disponibles",
                          font=ctk.CTkFont(size=14)).pack(pady=20)
        else:
            ctk.CTkLabel(content, text="Seleccione un médico:",
                          font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10, anchor="w")

            self.doctor_var = ctk.StringVar()
            for doc in doctors:
                ctk.CTkRadioButton(content, text=f"{doc.name} - {doc.specialty}",
                                     variable=self.doctor_var, value=str(doc.id),
                                     font=ctk.CTkFont(size=13)).pack(pady=5, anchor="w")

            ctk.CTkLabel(content, text="Fecha (YYYY-MM-DD):",
                          font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5), anchor="w")
            self.date_entry = ctk.CTkEntry(content, width=300, height=38,
                                             placeholder_text="2026-05-03",
                                             font=ctk.CTkFont(size=13))
            self.date_entry.pack(pady=5)

            ctk.CTkLabel(content, text="Hora (HH:MM):",
                          font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5), anchor="w")
            self.time_entry = ctk.CTkEntry(content, width=300, height=38,
                                            placeholder_text="09:00",
                                            font=ctk.CTkFont(size=13))
            self.time_entry.pack(pady=5)

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="RESERVAR",
                       font=ctk.CTkFont(size=14, weight="bold"),
                       width=150, height=45,
                       command=self.book_appointment).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_patient_menu).pack(side="left", padx=10)

    def book_appointment(self):
        try:
            doctor_id = int(self.doctor_var.get())
            date_str = self.date_entry.get()
            time_str = self.time_entry.get()
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            if not self.appointment_service.is_doctor_available(doctor_id, dt):
                messagebox.showerror("Error", "El médico ya tiene una cita a esa hora")
                return
            appt_id = self.appointment_service.create(doctor_id, self.current_patient.id, dt)
            self.audit_service.log(self.current_user.id, "book_appointment",
                                    f"Cita {appt_id} reservada con médico {doctor_id}")
            doctor = self.doctor_service.get_by_id(doctor_id)
            self.notification_service.send_appointment_confirmation(
                self.current_patient.email, self.current_patient.name, doctor.name, dt)
            messagebox.showinfo("Éxito", f"Cita reservada. Número: {appt_id}")
            self.show_patient_menu()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_cancel_appointment(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#d9534f", "#d9534f"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="CANCELAR CITA",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=40, pady=20)

        appointments = self.appointment_service.get_by_patient(self.current_patient.id)
        self.cancel_var = ctk.StringVar()

        ctk.CTkLabel(content, text="Seleccione la cita a cancelar:",
                      font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10, anchor="w")

        found = False
        for row in appointments:
            if row['status'] == AppointmentStatus.SCHEDULED.value:
                found = True
                text = f"{row['id']} - {row['datetime']} - Dr. {row['doctor_name']}"
                ctk.CTkRadioButton(content, text=text,
                                    variable=self.cancel_var, value=str(row['id']),
                                    font=ctk.CTkFont(size=13)).pack(pady=5, anchor="w")

        if not found:
            ctk.CTkLabel(content, text="No hay citas programadas",
                          font=ctk.CTkFont(size=14)).pack(pady=20)

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="CANCELAR CITA",
                       font=ctk.CTkFont(size=14, weight="bold"),
                       width=150, height=45,
                       fg_color=("#d9534f", "#d9534f"),
                       command=self.cancel_appointment).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_patient_menu).pack(side="left", padx=10)

    def cancel_appointment(self):
        try:
            appt_id = int(self.cancel_var.get())
            if messagebox.askyesno("Confirmar", "¿Está seguro de cancelar esta cita?"):
                self.appointment_service.cancel(appt_id)
                self.audit_service.log(self.current_user.id, "cancel_appointment",
                                        f"Cita {appt_id} cancelada")
                messagebox.showinfo("Éxito", "Cita cancelada")
                self.show_patient_menu()
        except:
            messagebox.showerror("Error", "Seleccione una cita")

    def show_my_appointments(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#1f538d", "#1f538d"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="MIS CITAS",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=40, pady=20)

        appointments = self.appointment_service.get_by_patient(self.current_patient.id)

        if not appointments:
            ctk.CTkLabel(content, text="No tienes citas registradas",
                          font=ctk.CTkFont(size=14)).pack(pady=20)
        else:
            for row in appointments:
                color = "#2ecc71" if row['status'] == "scheduled" else "#e74c3c" if row['status'] == "cancelled" else "#95a5a6"
                frame = ctk.CTkFrame(content, fg_color=("#2b2b2b", "#2b2b2b"))
                frame.pack(fill="x", pady=5, padx=10)

                btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
                btn_frame.pack(fill="x", padx=10, pady=5)

                ctk.CTkLabel(btn_frame, text=f"Cita #{row['id']} - {row['datetime']}",
                              font=ctk.CTkFont(size=14, weight="bold"),
                              text_color=color).pack(side="left", padx=(0, 10))
                ctk.CTkButton(btn_frame, text="EDITAR",
                               font=ctk.CTkFont(size=10),
                               width=70, height=25,
                               fg_color=("#f0ad4e", "#f0ad4e"),
                               command=lambda r=row: self.edit_appointment(r)).pack(side="right", padx=5)
                if row['status'] == "scheduled":
                    ctk.CTkButton(btn_frame, text="CANCELAR",
                                   font=ctk.CTkFont(size=10),
                                   width=80, height=25,
                                   fg_color=("#d9534f", "#d9534f"),
                                   command=lambda r=row: self.cancel_appointment_from_list(r)).pack(side="right", padx=5)

                ctk.CTkLabel(frame, text=f"Médico: {row['doctor_name']} | Estado: {row['status']}",
                              font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(0, 5))

        ctk.CTkButton(content, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_patient_menu).pack(pady=20)

    def edit_appointment(self, appointment_row):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#f0ad4e", "#f0ad4e"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=f"EDITAR CITA #{appointment_row['id']}",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=60, pady=30)

        ctk.CTkLabel(content, text=f"Fecha actual: {appointment_row['datetime'][:10]}",
                      font=ctk.CTkFont(size=14)).pack(pady=10, anchor="w")
        self.edit_date = ctk.CTkEntry(content, placeholder_text="Nueva fecha (YYYY-MM-DD)",
                                        width=300, height=40)
        self.edit_date.insert(0, appointment_row['datetime'][:10])
        self.edit_date.pack(pady=5)

        ctk.CTkLabel(content, text=f"Hora actual: {appointment_row['datetime'][11:16]}",
                      font=ctk.CTkFont(size=14)).pack(pady=(15, 5), anchor="w")
        self.edit_time = ctk.CTkEntry(content, placeholder_text="Nueva hora (HH:MM)",
                                       width=300, height=40)
        self.edit_time.insert(0, appointment_row['datetime'][11:16])
        self.edit_time.pack(pady=5)

        self.current_edit_appt = appointment_row

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="GUARDAR",
                       font=ctk.CTkFont(size=14, weight="bold"),
                       width=150, height=45,
                       command=self.save_edited_appointment).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_my_appointments).pack(side="left", padx=10)

    def save_edited_appointment(self):
        try:
            from datetime import datetime
            appt_id = self.current_edit_appt['id']
            doctor_id = self.current_edit_appt['doctor_id']
            date_str = self.edit_date.get()
            time_str = self.edit_time.get()
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

            if not self.appointment_service.is_doctor_available(doctor_id, dt):
                messagebox.showerror("Error", "El médico ya tiene una cita a esa hora")
                return

            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE appointments SET datetime = ? WHERE id = ?",
                           (dt.isoformat(), appt_id))
            conn.commit()
            self.db.close()

            self.audit_service.log(self.current_user.id, "edit_appointment",
                                    f"Cita {appt_id} editada a {dt}")
            messagebox.showinfo("Éxito", "Cita actualizada")
            self.show_my_appointments()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cancel_appointment_from_list(self, appointment_row):
        if messagebox.askyesno("Confirmar", "¿Cancelar esta cita?"):
            self.appointment_service.cancel(appointment_row['id'])
            self.audit_service.log(self.current_user.id, "cancel_appointment",
                                    f"Cita {appointment_row['id']} cancelada")
            messagebox.showinfo("Éxito", "Cita cancelada")
            self.show_my_appointments()

    def show_patient_data(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#5bc0de", "#5bc0de"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="MIS DATOS",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=60, pady=40)

        p = self.current_patient
        fields = [("Nombre:", p.name), ("DNI:", p.dni), ("Email:", p.email), ("Teléfono:", p.phone)]

        for label, value in fields:
            frame = ctk.CTkFrame(content, fg_color=("#2b2b2b", "#2b2b2b"))
            frame.pack(fill="x", pady=5)
            ctk.CTkLabel(frame, text=label, width=100,
                          font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(frame, text=value,
                          font=ctk.CTkFont(size=14)).pack(side="left", pady=10)

        ctk.CTkButton(content, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_patient_menu).pack(pady=20)

    def show_doctor_today(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#5cb85c", "#5cb85c"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="MIS CITAS DE HOY",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=40, pady=20)

        today = datetime.now().date()
        appointments = self.appointment_service.get_by_doctor(self.current_doctor.id, today)

        if not appointments:
            ctk.CTkLabel(content, text="No tiene citas programadas para hoy",
                          font=ctk.CTkFont(size=14)).pack(pady=20)
        else:
            for row in appointments:
                color = "#2ecc71" if row['status'] == "scheduled" else "#e74c3c"
                frame = ctk.CTkFrame(content, fg_color=("#2b2b2b", "#2b2b2b"))
                frame.pack(fill="x", pady=5, padx=10)
                ctk.CTkLabel(frame, text=f"{row['datetime'][11:16]} - {row['patient_name']}",
                              font=ctk.CTkFont(size=14, weight="bold"),
                              text_color=color).pack(anchor="w", padx=10, pady=5)
                ctk.CTkLabel(frame, text=f"Estado: {row['status']} | {row['patient_name']}",
                              font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(0, 5))

        ctk.CTkButton(content, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_doctor_menu).pack(pady=20)

    def show_doctor_all(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#5cb85c", "#5cb85c"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="TODAS MIS CITAS",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=40, pady=20)

        appointments = self.appointment_service.get_by_doctor(self.current_doctor.id)

        if not appointments:
            ctk.CTkLabel(content, text="No tiene citas registradas",
                          font=ctk.CTkFont(size=14)).pack(pady=20)
        else:
            for row in appointments:
                color = "#2ecc71" if row['status'] == "scheduled" else "#e74c3c" if row['status'] == "cancelled" else "#95a5a6"
                frame = ctk.CTkFrame(content, fg_color=("#2b2b2b", "#2b2b2b"))
                frame.pack(fill="x", pady=5, padx=10)
                ctk.CTkLabel(frame, text=f"{row['datetime']} - {row['patient_name']}",
                              font=ctk.CTkFont(size=14, weight="bold"),
                              text_color=color).pack(anchor="w", padx=10, pady=5)
                ctk.CTkLabel(frame, text=f"Estado: {row['status']}",
                              font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(0, 5))

        ctk.CTkButton(content, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_doctor_menu).pack(pady=20)

    def show_register_patient(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#5cb85c", "#5cb85c"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="REGISTRAR PACIENTE",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=60, pady=20)

        self.reg_entries = {}
        fields = [("Nombre completo", "name"), ("Email", "email"), ("Teléfono", "phone"), ("DNI", "dni")]

        for label, key in fields:
            ctk.CTkLabel(content, text=label, font=ctk.CTkFont(size=14)).pack(pady=(10, 5), anchor="w")
            entry = ctk.CTkEntry(content, width=350, height=38, font=ctk.CTkFont(size=13))
            entry.pack(pady=5)
            self.reg_entries[key] = entry

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="REGISTRAR",
                       font=ctk.CTkFont(size=14, weight="bold"),
                       width=150, height=45,
                       command=self.register_patient).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_admin_menu).pack(side="left", padx=10)

    def register_patient(self):
        try:
            name = self.reg_entries['name'].get()
            email = self.reg_entries['email'].get()
            phone = self.reg_entries['phone'].get()
            dni = self.reg_entries['dni'].get()
            if not all([name, email, phone, dni]):
                messagebox.showerror("Error", "Complete todos los campos")
                return
            patient_id = self.patient_service.create(name, email, phone, dni)
            self.audit_service.log(self.current_user.id, "register_patient",
                                    f"Paciente {name} registrado con ID {patient_id}")
            messagebox.showinfo("Éxito", f"Paciente registrado. ID: {patient_id}")
            self.show_admin_menu()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_register_doctor(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#5cb85c", "#5cb85c"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="REGISTRAR MÉDICO",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=60, pady=20)

        self.doc_entries = {}
        fields = [("Nombre completo", "name"), ("Especialidad", "specialty"),
                  ("Email", "email"), ("Teléfono", "phone")]

        for label, key in fields:
            ctk.CTkLabel(content, text=label, font=ctk.CTkFont(size=14)).pack(pady=(10, 5), anchor="w")
            entry = ctk.CTkEntry(content, width=350, height=38, font=ctk.CTkFont(size=13))
            entry.pack(pady=5)
            if key == "start":
                entry.insert(0, "08:00")
            elif key == "end":
                entry.insert(0, "17:00")
            self.doc_entries[key] = entry

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="REGISTRAR",
                       font=ctk.CTkFont(size=14, weight="bold"),
                       width=150, height=45,
                       command=self.register_doctor).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_admin_menu).pack(side="left", padx=10)

    def register_doctor(self):
        try:
            name = self.doc_entries['name'].get()
            specialty = self.doc_entries['specialty'].get()
            email = self.doc_entries['email'].get()
            phone = self.doc_entries['phone'].get()
            if not all([name, specialty, email, phone]):
                messagebox.showerror("Error", "Complete los campos obligatorios")
                return
            doctor_id = self.doctor_service.create(name, specialty, email, phone)
            self.audit_service.log(self.current_user.id, "register_doctor",
                                    f"Médico {name} registrado con ID {doctor_id}")
            messagebox.showinfo("Éxito", f"Médico registrado. ID: {doctor_id}")
            self.show_admin_menu()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_list_doctors(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#337ab7", "#337ab7"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="LISTA DE MÉDICOS",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=20, pady=20)

        doctors = self.doctor_service.get_all()

        if not doctors:
            ctk.CTkLabel(content, text="No hay médicos registrados",
                          font=ctk.CTkFont(size=14)).pack(pady=20)
        else:
            for doc in doctors:
                frame = ctk.CTkFrame(content, fg_color=("#2b2b2b", "#2b2b2b"))
                frame.pack(fill="x", pady=5, padx=10)

                btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
                btn_frame.pack(fill="x", padx=10, pady=5)

                ctk.CTkLabel(btn_frame, text=f"ID: {doc.id} - {doc.name}",
                              font=ctk.CTkFont(size=14, weight="bold"),
                              text_color="#5cb85c").pack(side="left", padx=(0, 10))
                ctk.CTkButton(btn_frame, text="EDITAR",
                               font=ctk.CTkFont(size=10),
                               width=70, height=25,
                               fg_color=("#f0ad4e", "#f0ad4e"),
                               command=lambda d=doc: self.edit_doctor(d)).pack(side="right", padx=5)
                ctk.CTkButton(btn_frame, text="ELIMINAR",
                               font=ctk.CTkFont(size=10),
                               width=80, height=25,
                               fg_color=("#d9534f", "#d9534f"),
                               command=lambda d=doc: self.delete_doctor(d)).pack(side="right", padx=5)

                ctk.CTkLabel(frame, text=f"Especialidad: {doc.specialty} | Email: {doc.email} | Tel: {doc.phone}",
                              font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(0, 5))

        ctk.CTkButton(content, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_admin_menu).pack(pady=20)

    def edit_doctor(self, doctor):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#f0ad4e", "#f0ad4e"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=f"EDITAR MÉDICO - {doctor.name}",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=60, pady=30)

        self.edit_doc_entries = {}
        fields = [("Nombre", doctor.name), ("Especialidad", doctor.specialty),
                  ("Email", doctor.email), ("Teléfono", doctor.phone)]

        for label, value in fields:
            ctk.CTkLabel(content, text=label, font=ctk.CTkFont(size=14)).pack(pady=(10, 5), anchor="w")
            entry = ctk.CTkEntry(content, width=350, height=38, font=ctk.CTkFont(size=13))
            entry.insert(0, value)
            entry.pack(pady=5)
            self.edit_doc_entries[label] = entry

        self.current_edit_doctor = doctor

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="GUARDAR",
                       font=ctk.CTkFont(size=14, weight="bold"),
                       width=150, height=45,
                       command=self.save_edited_doctor).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_list_doctors).pack(side="left", padx=10)

    def save_edited_doctor(self):
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE doctors SET name = ?, specialty = ?, email = ?, phone = ? WHERE id = ?",
                (self.edit_doc_entries["Nombre"].get(),
                 self.edit_doc_entries["Especialidad"].get(),
                 self.edit_doc_entries["Email"].get(),
                 self.edit_doc_entries["Teléfono"].get(),
                 self.current_edit_doctor.id)
            )
            conn.commit()
            self.db.close()
            self.audit_service.log(self.current_user.id, "edit_doctor",
                                    f"Médico {self.current_edit_doctor.id} actualizado")
            messagebox.showinfo("Éxito", "Médico actualizado")
            self.show_list_doctors()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_doctor(self, doctor):
        if messagebox.askyesno("Confirmar", f"¿Eliminar al médico {doctor.name}?"):
            self.doctor_service.delete(doctor.id)
            self.audit_service.log(self.current_user.id, "delete_doctor",
                                    f"Médico {doctor.id} eliminado")
            messagebox.showinfo("Éxito", "Médico eliminado")
            self.show_list_doctors()

    def show_list_patients(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#337ab7", "#337ab7"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="LISTA DE PACIENTES",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=20, pady=20)

        patients = self.patient_service.get_all()

        if not patients:
            ctk.CTkLabel(content, text="No hay pacientes registrados",
                          font=ctk.CTkFont(size=14)).pack(pady=20)
        else:
            for p in patients:
                frame = ctk.CTkFrame(content, fg_color=("#2b2b2b", "#2b2b2b"))
                frame.pack(fill="x", pady=5, padx=10)

                btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
                btn_frame.pack(fill="x", padx=10, pady=5)

                ctk.CTkLabel(btn_frame, text=f"ID: {p.id} - {p.name}",
                              font=ctk.CTkFont(size=14, weight="bold"),
                              text_color="#5cb85c").pack(side="left", padx=(0, 10))
                ctk.CTkButton(btn_frame, text="EDITAR",
                               font=ctk.CTkFont(size=10),
                               width=70, height=25,
                               fg_color=("#f0ad4e", "#f0ad4e"),
                               command=lambda pt=p: self.edit_patient(pt)).pack(side="right", padx=5)
                ctk.CTkButton(btn_frame, text="ELIMINAR",
                               font=ctk.CTkFont(size=10),
                               width=80, height=25,
                               fg_color=("#d9534f", "#d9534f"),
                               command=lambda pt=p: self.delete_patient(pt)).pack(side="right", padx=5)

                ctk.CTkLabel(frame, text=f"DNI: {p.dni} | Email: {p.email} | Tel: {p.phone}",
                              font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(0, 5))

        ctk.CTkButton(content, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_admin_menu).pack(pady=20)

    def edit_patient(self, patient):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#f0ad4e", "#f0ad4e"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text=f"EDITAR PACIENTE - {patient.name}",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=60, pady=30)

        self.edit_pat_entries = {}
        fields = [("Nombre", patient.name), ("Email", patient.email),
                  ("Teléfono", patient.phone), ("DNI", patient.dni)]

        for label, value in fields:
            ctk.CTkLabel(content, text=label, font=ctk.CTkFont(size=14)).pack(pady=(10, 5), anchor="w")
            entry = ctk.CTkEntry(content, width=350, height=38, font=ctk.CTkFont(size=13))
            entry.insert(0, value)
            entry.pack(pady=5)
            self.edit_pat_entries[label] = entry

        self.current_edit_patient = patient

        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(btn_frame, text="GUARDAR",
                       font=ctk.CTkFont(size=14, weight="bold"),
                       width=150, height=45,
                       command=self.save_edited_patient).pack(side="left", padx=10)

        ctk.CTkButton(btn_frame, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_list_patients).pack(side="left", padx=10)

    def save_edited_patient(self):
        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE patients SET name = ?, email = ?, phone = ?, dni = ? WHERE id = ?",
                (self.edit_pat_entries["Nombre"].get(),
                 self.edit_pat_entries["Email"].get(),
                 self.edit_pat_entries["Teléfono"].get(),
                 self.edit_pat_entries["DNI"].get(),
                 self.current_edit_patient.id)
            )
            conn.commit()
            self.db.close()
            self.audit_service.log(self.current_user.id, "edit_patient",
                                    f"Paciente {self.current_edit_patient.id} actualizado")
            messagebox.showinfo("Éxito", "Paciente actualizado")
            self.show_list_patients()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_patient(self, patient):
        if messagebox.askyesno("Confirmar", f"¿Eliminar al paciente {patient.name}?"):
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM patients WHERE id = ?", (patient.id,))
            conn.commit()
            self.db.close()
            self.audit_service.log(self.current_user.id, "delete_patient",
                                    f"Paciente {patient.id} eliminado")
            messagebox.showinfo("Éxito", "Paciente eliminado")
            self.show_list_patients()

    def show_all_appointments(self):
        self.clear_window()

        header = ctk.CTkFrame(self.root, height=80, fg_color=("#337ab7", "#337ab7"))
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="TODAS LAS CITAS",
                      font=ctk.CTkFont(size=22, weight="bold"),
                      text_color="white").pack(pady=20)

        content = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        content.pack(expand=True, fill="both", padx=20, pady=20)

        appointments = self.appointment_service.get_all()

        if not appointments:
            ctk.CTkLabel(content, text="No hay citas registradas",
                          font=ctk.CTkFont(size=14)).pack(pady=20)
        else:
            for row in appointments:
                color = "#2ecc71" if row['status'] == "scheduled" else "#e74c3c" if row['status'] == "cancelled" else "#95a5a6"
                frame = ctk.CTkFrame(content, fg_color=("#2b2b2b", "#2b2b2b"))
                frame.pack(fill="x", pady=5, padx=10)
                ctk.CTkLabel(frame, text=f"Cita #{row['id']} - {row['datetime']}",
                              font=ctk.CTkFont(size=14, weight="bold"),
                              text_color=color).pack(anchor="w", padx=10, pady=5)
                ctk.CTkLabel(frame, text=f"Paciente: {row['patient_name']} | Médico: {row['doctor_name']} | Estado: {row['status']}",
                              font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(0, 5))

        ctk.CTkButton(content, text="VOLVER",
                       font=ctk.CTkFont(size=14),
                       width=150, height=45,
                       fg_color="gray",
                       command=self.show_admin_menu).pack(pady=20)

    def logout(self):
        if self.current_user:
            self.audit_service.log(self.current_user.id, "logout", None)
        self.show_login()


if __name__ == "__main__":
    app = ClinicGUI()
    app.run()
