# Listado de Módulos — Sistema de Gestión para Gimnasios

En este documento detallan los módulos funcionales del sistema

---

## 1. Módulo de Alumnos

**Descripción:** Gestión centralizada de los datos de cada alumno y su ficha de salud básica

**Funcionalidades:**
- Alta, edición y baja lógica de alumnos (nombre, DNI, contacto).
- Generación del código de acceso al dar de alta y regeneración ante pérdida (el código se muestra una única vez).
- Configuración de la meta semanal de asistencias de cada alumno.
- Registro de ficha de salud (problemas cardíacos, lesiones, observaciones).
- Listado general de alumnos con filtro por estado (activo / por vencer / vencido).

---

## 2. Módulo de Planes e Inscripciones

**Descripción:** Catálogo de planes ofrecidos por el gimnasio y gestión de la inscripción de cada alumno a un plan

**Funcionalidades:**
- Alta y edición de planes (nombre, duración, precio y tipo: por tiempo o por clases; en los planes por clases, también la cantidad de clases).
- Inscripción de un alumno a un plan, con cálculo automático de fecha de vencimiento y, en planes por clases, inicialización del saldo de clases.
- Actualización automática del estado de la inscripción (activo / por vencer / vencido) en función de la fecha actual y, en planes por clases, del saldo de clases.
- Detalle de los planes por clases en [`planes_por_clases.md`](./planes_por_clases.md).
---

## 3. Módulo de Pagos

**Descripción:** Registro de cobranzas asociadas a cada inscripción

**Funcionalidades:**
- Alta de pagos, con fecha, monto y método de pago (efectivo, transferencia, débito, crédito).
- Renovación de una inscripción, vigente o vencida, a partir de un nuevo pago.
- Historial de pagos por alumno.

---

## 4. Módulo de Asistencia

**Descripción:** Registro diario de ingreso de los alumnos al gimnasio.

**Funcionalidades:**
- Check-in manual: búsqueda del alumno y registro de ingreso con fecha y hora, asociado a su inscripción vigente.
- Validación para evitar check-ins duplicados dentro de una ventana de 2 horas.
- En planes por clases, descuento de una clase por ingreso y rechazo del ingreso si el saldo es cero.
- Historial de asistencia por alumno.
- Base para los indicadores de concurrencia del dashboard.

---

## 5. Módulo de Dashboard Administrativo

**Descripción:** Panel de indicadores para el personal del gimnasio.

**Funcionalidades:**
- Facturación total del mes y desglosada por método de pago.
- Cantidad de alumnos activos, por vencer y vencidos.
- Alumnos nuevos del mes.
- Asistencias registradas por semana.
- Cuotas vencidas pendientes de cobro.
- Ingresos proyectados del mes en curso.

---

## 6. Módulo de Panel del Alumno

**Descripción:** Vista de autoconsulta de solo lectura para que el propio alumno acceda a su información. El acceso requiere DNI y código de acceso, sin contraseña.

**Funcionalidades:**
- Acceso con DNI y código de acceso, con bloqueo temporal tras 5 intentos fallidos.
- Consulta de estado de cuota (activo / por vencer / vencido) y, en planes por clases, clases restantes.
- Consulta de historial de asistencia propio.
- Checklist personal simple de objetivos.
- Consulta de las rutinas ya aprobadas por el entrenador. No muestra la ficha de salud.

---

## 7. Módulo de Rutinas 

**Descripción:** Banco de rutinas físicas básicas, cargado y mantenido por el entrenador.

**Funcionalidades:**
- Alta y edición de rutinas (calentamiento, movilidad articular, vuelta a la calma), exclusivas del perfil entrenador.
- Cada rutina indica contraindicaciones.
- Aprobación o rechazo de rutinas sugeridas por el Asistente de IA.

---

## 8. Módulo de Asistente de IA

**Descripción:** Componente que sugiere rutinas del banco predefinido según el perfil de salud del alumno, sin generar contenido nuevo.

**Funcionalidades:**
- Filtrado de rutinas compatibles con la ficha de salud del alumno.
- Generación de sugerencia en estado "pendiente" hasta aprobación del entrenador.

---

## 9. Módulo de Configuración

**Descripción:** Parámetros generales del sistema, administrables solo por el administrador.

**Funcionalidades:**
- Datos generales del gimnasio (nombre, contacto).
- Cantidad de días de anticipación para "por vencer".
- Métodos de pago habilitados.

## 10. Módulo de Gestión de Entrenadores

**Descripción:** Administración de los entrenadores que cargan rutinas y aprueban sugerencias del Asistente de IA.

**Funcionalidades:**
- Alta y edición de entrenadores (nombre, contacto).
- Asociación de cada rutina cargada y cada aprobación al entrenador correspondiente.

## 11. Módulo de Usuarios y Seguridad

**Descripción:** Autenticación del personal y control de acceso según el perfil de cada usuario.

**Funcionalidades:**
- Inicio de sesión del personal con usuario y contraseña (almacenada con hash), con bloqueo temporal tras 5 intentos fallidos.
- Alta y desactivación de usuarios (administrador o entrenador) y restablecimiento de contraseñas, a cargo del administrador.
- Control de las funciones habilitadas según el perfil, validado en el backend en cada petición.
- Registro en el log de las acciones sensibles.
- Detalle de perfiles y permisos en [`seguridad_y_permisos.md`](./seguridad_y_permisos.md).

## Resumen de trazabilidad con el modelo de datos

| Módulo | Tablas relacionadas |
|---|---|
| 1. Alumnos | `alumnos`, `ficha_salud`, `metas_alumno` |
| 2. Planes e Inscripciones | `planes`, `inscripciones` |
| 3. Pagos | `pagos`, `inscripciones` |
| 4. Asistencia | `asistencias`, `inscripciones` |
| 5. Dashboard Administrativo | *(consultas agregadas sobre `pagos`, `inscripciones`, `asistencias`)* |
| 6. Panel del Alumno | `alumnos`, `inscripciones`, `asistencias`, `rutinas_asignadas`, `metas_alumno` |
| 7. Rutinas | `rutinas`, `entrenadores` |
| 8. Asistente de IA | `rutinas`, `rutinas_asignadas`, `ficha_salud` |
| 9. Configuración | `configuracion` |
| 10. Gestión de Entrenadores | `entrenadores` |
| 11. Usuarios y Seguridad | `usuarios`, `entrenadores` |

El esquema completo de estas tablas se encuentra en [`/database/schema.sql`](../database/schema.sql).