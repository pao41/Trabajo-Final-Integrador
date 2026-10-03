# Criterios de Aceptación — Sistema de Gestión para Gimnasios

Precondición, acción disparadora y resultado esperado para cada Requerimiento Funcional.

| # | Precondición | Acción | Resultado esperado |
|---|---|---|---|
| RF01 | No existe un alumno con ese DNI. |El administrador completa el alta con DNI, nombre y contacto. | El alumno queda registrado, activo, con un código de acceso único generado. |
| RF02 | El alumno está registrado. | El administrador carga los datos de salud declarados. | La ficha de salud queda asociada al alumno y disponible para el Asistente de IA. |
| RF03 | — | El administrador crea o edita un plan (nombre, duración, precio, tipo). | El plan queda disponible para asignar en una inscripción. |
| RF04 | El alumno y el plan existen. | El administrador inscribe al alumno en un plan. | Se crea la inscripción con fecha de vencimiento calculada automáticamente. |
| RF05 | Existe una inscripción. | El sistema evalúa la fecha actual contra el vencimiento. | El estado pasa a `activo`, `por_vencer` o `vencido`. |
| RF06 | Existe una inscripción. | El administrador registra un pago (fecha, monto, método). | El pago queda registrado y la inscripción se renueva/extiende. |
| RF07 | El alumno está registrado. | El staff registra su ingreso. | Se crea el registro de asistencia, salvo duplicado en la misma franja horaria. |
| RF08 | Existen pagos, inscripciones y asistencias cargadas. | El administrador abre el dashboard. | Se muestran facturación, alumnos nuevos, asistencias semanales, cuotas vencidas e ingresos proyectados actualizados. |
| RF09 | Existen alumnos con inscripciones. | El administrador filtra el listado por estado. | Se muestra solo a los alumnos cuyo estado coincide con el filtro. |
| RF10 | El alumno tiene código de acceso válido. | El alumno ingresa su código o DNI. | Se muestra su estado de cuota, asistencia y checklist personal. |
| RF11 | El entrenador está registrado (RN24). | El entrenador carga una rutina con tipo y contraindicaciones. | La rutina queda disponible en el banco, asociada a ese entrenador. |
| RF12 | El alumno tiene ficha de salud y existen rutinas compatibles. | El alumno solicita una sugerencia. | El sistema devuelve una rutina del banco compatible con su ficha de salud, en estado `pendiente`. |
| RF13 | Existe una rutina sugerida en estado `pendiente`. | El entrenador aprueba o rechaza la sugerencia. | El estado cambia a `aprobada` o `rechazada`; solo las aprobadas son visibles para el alumno. |
| RF14 | El alumno tiene pagos registrados. | Se da de baja al alumno o cambia de plan. | El historial de pagos e inscripciones previas permanece intacto y consultable. |
| RF15 | El alumno reporta pérdida de su código. | El administrador solicita la regeneración. | Se genera un nuevo código de acceso único para el alumno. |
| RF16 | — | El administrador modifica un parámetro general. | El nuevo valor se aplica a los cálculos y validaciones del sistema. |
| RF17 | — | El administrador da de alta o edita un entrenador. | El entrenador queda disponible para cargar y aprobar rutinas. |
| RF18 | Existe al menos un entrenador registrado. | Se carga una rutina o se aprueba una sugerencia. | La acción queda asociada al entrenador que la realizó (trazabilidad). |
| RF19 | El alumno está registrado. | El administrador configura su meta semanal de asistencias. | El Panel del Alumno calcula el checklist comparando asistencias de la semana contra la meta. |
