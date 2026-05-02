import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class NotificationService:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587,
                 sender_email="clinica@medicalcare.com", sender_password=""):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

    def send_appointment_confirmation(self, patient_email, patient_name, doctor_name, appointment_datetime):
        subject = "Confirmación de Cita - Clínica Medical Care"
        body = f"""
Estimado/a {patient_name},

Su cita ha sido confirmada:

📅 Fecha: {appointment_datetime.strftime('%Y-%m-%d')}
🕐 Hora: {appointment_datetime.strftime('%H:%M')}
👨‍⚕️ Médico: Dr. {doctor_name}

Por favor llegue 15 minutos antes de su cita.

Gracias por confiar en Clínica Medical Care.
        """
        self._send_email(patient_email, subject, body)

    def send_appointment_cancellation(self, patient_email, patient_name, doctor_name, appointment_datetime):
        subject = "Cancelación de Cita - Clínica Medical Care"
        body = f"""
Estimado/a {patient_name},

Su cita ha sido cancelada:

📅 Fecha: {appointment_datetime.strftime('%Y-%m-%d')}
🕐 Hora: {appointment_datetime.strftime('%H:%M')}
👨‍⚕️ Médico: Dr. {doctor_name}

Puede reprogramar su cita contactándonos.
        """
        self._send_email(patient_email, subject, body)

    def send_appointment_reminder(self, patient_email, patient_name, doctor_name, appointment_datetime):
        subject = "Recordatorio de Cita - Mañana"
        body = f"""
Estimado/a {patient_name},

Le recordamos que tiene una cita programada para mañana:

📅 Fecha: {appointment_datetime.strftime('%Y-%m-%d')}
🕐 Hora: {appointment_datetime.strftime('%H:%M')}
👨‍⚕️ Médico: Dr. {doctor_name}

¡Esperamos verle pronto!
        """
        self._send_email(patient_email, subject, body)

    def _send_email(self, recipient, subject, body):
        if not self.sender_password:
            print(f"[MOCK] Email enviado a {recipient}: {subject}")
            return
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            print(f"Error enviando email: {e}")
