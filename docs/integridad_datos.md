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
| RN25 — una meta por alumno, entre 1 y 7 asistencias | `UNIQUE` + `CHECK (BETWEEN 1 AND 7)` | `metas_alumno` |
| RN22 — tipos de rutina permitidos | `CHECK` (`calentamiento`, `movilidad`, `vuelta_a_la_calma`) | `rutinas.tipo` |
| RN21, RN24 — una sugerencia pendiente no tiene entrenador ni fecha; una aprobada o rechazada tiene ambos | `CHECK chk_validacion_coherente` + `FK` a `entrenadores` | `rutinas_asignadas` |
| RN24 — el entrenador debe existir | `FK` | `rutinas.entrenador_id`, `rutinas_asignadas.entrenador_id` |
| RN34 — perfiles de usuario válidos | `CHECK` (`administrador`, `entrenador`) | `usuarios.rol` |
| RN35 — el usuario entrenador está vinculado a un entrenador y los demás perfiles no | `CHECK chk_usuario_entrenador` + `UNIQUE` | `usuarios.entrenador_id` |
| Usuario único | `UNIQUE` | `usuarios.nombre_usuario` |
| RN33, RN37 — las credenciales no se guardan en texto plano | Solo existen las columnas `*_hash` | `usuarios.password_hash`, `alumnos.codigo_acceso_hash` |
| Configuración única | `id` fijo en 1 con `CHECK (id = 1)`: no admite una segunda fila | `configuracion` |
| RN09 — días de aviso positivos | `CHECK (dias_aviso_vencimiento > 0)` | `configuracion` |

## 2. Reglas controladas por la aplicación

Estas reglas dependen de cálculos, del tiempo o de varias tablas a la vez, por lo que no se expresan como una restricción simple. La aplicación las valida antes de escribir en la base.

| Regla | Por qué no la controla la base | Cómo se resuelve |
|---|---|---|
| RN12 — ventana de 2 horas entre check-ins | Compara con el ingreso anterior | El backend consulta el último ingreso del alumno antes de insertar. Podría reforzarse en el futuro con una restricción de exclusión sobre rangos de tiempo |
| RN02, RN03, RN04 — cálculo del vencimiento | Es un cálculo con fechas | Lo calcula el servicio de pagos |
| RN01, RN09 — estado de la inscripción | Depende de la fecha actual | Se recalcula al consultar o al registrar un pago |
| RN30, RN32 — descuento y renovación de clases | Involucra varias tablas | Ver "Operaciones atómicas" |
| Coherencia entre `planes.tipo` y `inscripciones.clases_restantes` | Compara dos tablas | La aplicación inicializa el saldo solo para planes por clases |
| RN05 — el monto del pago es el precio completo del plan | Compara dos tablas | El backend toma el monto del plan |
| RN20 — rutinas compatibles con la ficha de salud | Filtro de negocio | El backend filtra por contraindicaciones |
| RN34, RN36 — permisos por perfil | Depende del usuario autenticado | Dependencia de autorización en el backend |
| RN38 — bloqueo por intentos fallidos | Depende del tiempo | Límite de intentos en el backend |

## 3. Operaciones atómicas

Estas operaciones modifican varias tablas y deben ejecutarse dentro de una **transacción**: si un paso falla, no se aplica ninguno.

| Operación | Pasos que se ejecutan juntos |
|---|---|
| Registrar ingreso en plan por clases | Insertar la asistencia con su `inscripcion_id` + descontar una clase de `clases_restantes` |
| Registrar un pago | Insertar el pago + actualizar `fecha_vencimiento`, `clases_restantes` y `estado` de la inscripción |
| Aprobar o rechazar una sugerencia | Actualizar `estado`, `entrenador_id` y `fecha_validacion` en un solo UPDATE (lo exige `chk_validacion_coherente`) |
