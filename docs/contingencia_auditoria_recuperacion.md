# Auditoría, Contingencia y Recuperación — Sistema de Gestión para Gimnasios

Este documento describe, a nivel conceptual, cómo se registran las acciones importantes, cómo se sigue operando si el sistema falla y cómo se recuperan los datos. Complementa [`arquitectura.md`](./arquitectura.md) y [`seguridad_y_permisos.md`](./seguridad_y_permisos.md).

## 1. Auditoría

### Qué se registra y dónde

| Fuente | Qué permite saber | Regla |
|---|---|---|
| Tablas de negocio (`pagos`, `inscripciones`, `asistencias`, `rutinas`, `rutinas_asignadas`) | Qué ocurrió y cuándo; en rutinas, qué entrenador actuó. No se borran físicamente (`ON DELETE RESTRICT`) | RN28 |
| Log del backend | Quién ejecutó una acción sensible, cuál fue y cuándo | RN40 |

### Formato del registro de acciones sensibles

Cada acción sensible genera una línea de log con: fecha y hora, usuario (o "alumno" en el Panel del Alumno), acción, entidad afectada y resultado (éxito o rechazo).

Ejemplo: `2026-11-03 10:42:15 | usuario=admin | BAJA_ALUMNO | alumnos#12 | OK`
