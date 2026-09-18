# Listado de Módulos — Sistema de Gestión para Gimnasios

En este documento detallan los módulos funcionales del sistema

---

## 1. Módulo de Alumnos

**Descripción:** Gestión centralizada de los datos de cada alumno y su ficha de salud básica

**Funcionalidades:**
- Alta, edición y baja de alumnos (nombre, DNI, contacto, código de acceso).
- Registro de ficha de salud (problemas cardíacos, lesiones, observaciones).
- Listado general de alumnos con filtro por estado (activo / por vencer / vencido).

---

## 2. Módulo de Planes e Inscripciones

**Descripción:** Catálogo de planes ofrecidos por el gimnasio y gestión de la inscripción de cada alumno a un plan

**Funcionalidades:**
- Alta y edición de planes (nombre, duración, precio, tipo: por tiempo o por clases).
- Inscripción de un alumno a un plan, con cálculo automático de fecha de vencimiento.
- Actualización automática del estado de la inscripción (activo / por vencer / vencido) en función de la fecha actual.

---

## 3. Módulo de Pagos

**Descripción:** Registro de cobranzas asociadas a cada inscripción

**Funcionalidades:**
- Alta de pagos, con fecha, monto y método de pago (efectivo, transferencia, débito, crédito).
- Renovación de una inscripción vencida a partir de un nuevo pago.
- Historial de pagos por alumno.

---