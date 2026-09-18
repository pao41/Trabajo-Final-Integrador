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

## 4. Módulo de Asistencia

**Descripción:** Registro diario de ingreso de los alumnos al gimnasio.

**Funcionalidades:**
- Check-in manual: búsqueda del alumno y registro de ingreso con fecha y hora.
- Historial de asistencia por alumno.
- Base para los indicadores de concurrencia del dashboard.

---

## 5. Módulo de Dashboard Administrativo

**Descripción:** Panel de indicadores para el personal del gimnasio.

**Funcionalidades:**
- Facturación total del mes.
- Facturación desglosada por método de pago.
- Cantidad de alumnos activos, por vencer y vencidos.

---

## 6. Módulo de Panel del Alumno

**Descripción:** Vista de autoconsulta para que el propio alumno acceda a su información, sin necesidad de un sistema de login con contraseña.

**Funcionalidades:**
- Acceso mediante código simple o DNI.
- Consulta de estado de cuota (activo / por vencer / vencido).
- Consulta de historial de asistencia propio.
- Checklist personal simple de objetivos.

---

## 7. Módulo de Rutinas y Asistente de IA

**Descripción:** Sección de rutinas físicas básicas, con un asistente que sugiere rutinas dentro de un banco predefinido, sujeto a validación del entrenador.

**Funcionalidades:**
- Banco de rutinas predefinido (calentamiento, movilidad articular, vuelta a la calma), cargado y mantenido por el entrenador.
- Cada rutina indica contraindicaciones.
- El asistente filtra rutinas compatibles con la ficha de salud del alumno — no genera ejercicios nuevos.
- Toda rutina sugerida queda en estado "pendiente" hasta que un entrenador la aprueba para ese alumno en particular.
- Mensaje explícito de que la sugerencia es orientativa y no reemplaza la supervisión del entrenador.

---

El esquema completo de estas tablas se encuentra en: /database/schema.sql
