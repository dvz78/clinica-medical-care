# Sistema de Gestión de Citas Médicas - Clínica Medical Care

Sistema completo para gestión de citas entre médicos y pacientes en clínicas.

## Tecnologías

- **Python 3** - Lenguaje principal
- **SQLite** - Base de datos embebida para persistencia
- **CustomTkinter** - Interfaz gráfica moderna (estilo Windows 11)
- **Pillow** - Procesamiento de imágenes

## Características Implementadas

✅ **Sistema de Roles**: Admin, Médico, Paciente con accesos independientes
✅ **Interfaz Gráfica Moderna**: Botones, formularios, ventanas independientes
✅ **Notificaciones por Email**: Confirmación y cancelación de citas
✅ **Reportes y Estadísticas**: Citas por médico, especialidad, tasa de cancelación
✅ **Auditoría**: Log completo de acciones de usuarios
✅ **Múltiples Médicos y Pacientes**: Gestión completa con SQLite
✅ **Persistencia de Datos**: Base de datos local sin configuración adicional

## Estructura

```
├── gui/
│   ├── app.py           # Interfaz gráfica (CustomTkinter)
│   └── web_app.py      # Versión web (NiceGUI - opcional)
├── models/              # Modelos de datos
│   ├── doctor.py
│   ├── patient.py
│   ├── appointment.py
│   └── user.py
├── services/            # Lógica de negocio
│   ├── database.py
│   ├── doctor_service.py
│   ├── patient_service.py
│   ├── appointment_service.py
│   ├── user_service.py
│   ├── audit_service.py
│   ├── report_service.py
│   └── notification_service.py
├── data/                # Base de datos (se crea automáticamente)
│   └── clinic.db
├── run_gui.py          # Lanzador interfaz gráfica
├── requirements.txt     # Dependencias
└── README.md
```

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

### 1. Cargar Datos de Ejemplo (Opcional)
```bash
python3 load_demo.py
```
Esto carga médicos, pacientes, usuarios y citas de ejemplo (los mostrados arriba).

### 2. Ejecutar la Aplicación
```bash
python3 run_gui.py
```

**Credenciales de Ejemplo:**
- **Admin**: `admin` / `admin123`
- **Médico**: `juan_perez` / `doctor123`
- **Paciente**: DNI `12345678A`, `87654321B`

## Funcionalidades de Edición

✅ **Editar Médicos**: Botón "EDITAR" junto a cada médico en la lista
✅ **Eliminar Médicos**: Botón "ELIMINAR" para borrar médicos
✅ **Editar Pacientes**: Botón "EDITAR" junto a cada paciente
✅ **Eliminar Pacientes**: Botón "ELIMINAR" para borrar pacientes
✅ **Editar Citas**: Botón "EDITAR" en "Mis Citas" para cambiar fecha/hora
✅ **Cancelar Citas**: Botón "CANCELAR" para cancelar citas programadas

### Funcionalidades por Rol

**Paciente:**
- Reservar citas
- Cancelar citas
- Ver sus citas
- Actualizar datos

**Médico:**
- Ver citas del día
- Ver todas sus citas

**Administrador:**
- Registrar médicos y pacientes
- Crear usuarios con roles
- Ver reportes y estadísticas
- Consultar log de auditoría
- Gestionar todas las citas

## Licencia

Este proyecto está bajo la **Licencia de Uso No Comercial**.

- ✅ Uso personal y educativo: **Gratuito**
- ✅ Modificación para uso propio: **Permitida**
- ❌ Uso comercial: **Prohibido sin autorización**

Si deseas usar este sistema con fines comerciales (vender, licenciar, o integrar en producto comercial), debes contactar al creador:

📧 **Contacto**: [Tu Email Aquí]

Ver el archivo [LICENSE](LICENSE) para más detalles.

## Funcionalidades

1. **Registro de pacientes** - Registrar nuevos pacientes con DNI, email y teléfono
2. **Reserva de citas** - Pacientes pueden reservar citas con médicos disponibles
3. **Cancelación de citas** - Cancelar citas existentes
4. **Consulta de citas** - Ver citas por paciente o médico
5. **Listado de médicos** - Ver todos los médicos registrados
6. **Listado de pacientes** - Ver todos los pacientes registrados
7. **Listado de citas** - Ver todas las citas del sistema

## Menú Principal

- `1` - Registrar paciente
- `2` - Reservar cita
- `3` - Cancelar cita
- `4` - Ver citas de un paciente
- `5` - Ver citas de un médico
- `6` - Listar médicos
- `7` - Listar pacientes
- `8` - Listar todas las citas
- `0` - Salir
