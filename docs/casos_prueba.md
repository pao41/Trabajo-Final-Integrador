# Casos de Prueba — Sistema de Gestión para Gimnasios

| ID | Objetivo | Precondición | Pasos | Resultado esperado |
|---|---|---|---|---|
| CP01 | Alta de alumno exitosa | No existe alumno con ese DNI | Completar formulario de alta con datos válidos | Alumno creado, activo, con código de acceso único |
| CP02 | Rechazar DNI duplicado | Ya existe un alumno con ese DNI (RN13) | Intentar dar de alta otro alumno con el mismo DNI | El sistema rechaza el alta e informa el motivo |
| CP03 | Cálculo correcto de vencimiento | Alumno inscripto en un plan de 30 días | Registrar pago el día de inicio | `fecha_vencimiento` = fecha de pago + 30 días (RN02) |
| CP04 | Reactivación tras pago vencido | Inscripción en estado `vencido` | Registrar un nuevo pago | El plan se reactiva desde la fecha del nuevo pago, sin recuperar días perdidos (RN04) |