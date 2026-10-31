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

### Qué no se registra

Contraseñas, códigos de acceso ni datos de salud, para no exponer información sensible en los logs.

### Quién consulta y por cuánto tiempo

- El administrador consulta el log desde el servicio de hosting del backend.
- Se conserva mientras el proveedor lo permita; si hace falta guardarlo más tiempo, se exporta periódicamente.

## 2. Contingencia (continuidad operativa)

| Escenario | Impacto | Respuesta |
|---|---|---|
| Sin internet o sistema caído en horario de atención | No se pueden registrar ingresos ni pagos | Se usa la planilla manual de contingencia (ver abajo); los datos se cargan al volver el servicio (RN41) |
| Falla del servicio de hosting del backend | El sistema no responde | Se espera la restauración del proveedor; mientras tanto, planilla manual. El código se puede redesplegar desde GitHub |
| Pérdida o corrupción de datos | Se pierde información de alumnos, pagos o asistencias | Procedimiento de recuperación (sección 3) |
| Carga errónea de un dato | Un pago o ingreso mal cargado | El registro no se elimina (RN28): el administrador corrige el dato y la modificación queda registrada en el log (RN40) |
| Contraseña de personal olvidada | Un usuario no puede entrar | El administrador restablece la contraseña (RF23) |
| Código de acceso de alumno perdido | El alumno no puede ver su panel | El personal regenera el código (RF15) |
