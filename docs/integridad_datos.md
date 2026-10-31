# Integridad de Datos — Reglas controladas por la Base de Datos

La aplicación valida los datos primero, para dar mensajes claros al usuario. La base de datos actúa como última línea de defensa: aunque la aplicación tenga un error, hay reglas que PostgreSQL no deja violar. Este documento indica qué reglas de negocio se controlan en cada nivel. Las restricciones están definidas en [`/database/schema.sql`](../database/schema.sql).

## 1. Reglas controladas por la base de datos

| Regla | Mecanismo en la base de datos | Tabla.columna |
|---|---|---|
| RN13 — DNI único | `UNIQUE` | `alumnos.dni` |
| RN14, RN28, RF14 — el historial no se borra | `ON DELETE RESTRICT` en todas las claves foráneas: no se puede eliminar un alumno, plan, inscripción o entrenador con registros asociados | Todas las FK |
| RN01 — estados válidos de la inscripción | `CHECK` (`activo`, `por_vencer`, `vencido`) | `inscripciones.estado` |
| RN02 — coherencia de fechas | `CHECK (fecha_vencimiento >= fecha_inicio)` | `inscripciones` |
| RN29 — plan por clases con cantidad, plan por tiempo sin cantidad | `CHECK chk_plan_clases` | `planes.tipo` y `planes.cantidad_clases` |
| Duración y precio positivos | `CHECK (duracion_dias > 0)`, `CHECK (precio > 0)` | `planes` |
| RN30 — el saldo de clases nunca es negativo | `CHECK chk_inscripcion_saldo` | `inscripciones.clases_restantes` |
| Pagos con monto válido | `CHECK (monto > 0)` | `pagos.monto` |
| RN08, RN27 — método de pago válido y sin datos de tarjeta | `CHECK` (`efectivo`, `transferencia`, `debito`, `credito`); no existen columnas para datos de tarjeta | `pagos.metodo_pago` |
| Relación 1 a 1 entre alumno y ficha de salud | `UNIQUE` + `FK` | `ficha_salud.alumno_id` |