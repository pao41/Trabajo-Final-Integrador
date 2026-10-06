# Casos de Prueba — Sistema de Gestión para Gimnasios

| ID | Objetivo | Precondición | Pasos | Resultado esperado |
|---|---|---|---|---|
| CP01 | Alta de alumno exitosa | No existe alumno con ese DNI | Completar formulario de alta con datos válidos | Alumno creado, activo, con código de acceso único |
| CP02 | Rechazar DNI duplicado | Ya existe un alumno con ese DNI (RN13) | Intentar dar de alta otro alumno con el mismo DNI | El sistema rechaza el alta e informa el motivo |
| CP03 | Cálculo correcto de vencimiento | Alumno inscripto en un plan de 30 días | Registrar pago el día de inicio | `fecha_vencimiento` = fecha de pago + 30 días (RN02) |
| CP04 | Reactivación tras pago vencido | Inscripción en estado `vencido` | Registrar un nuevo pago | El plan se reactiva desde la fecha del nuevo pago, sin recuperar días perdidos (RN04) |
| CP05 | Dashboard refleja facturación por método | Existen pagos con distintos métodos | Abrir el dashboard | El total coincide con la suma real de pagos, desglosado correctamente por método |
| CP06 | Rechazar check-in duplicado | Alumno registró ingreso hace 1 hora | Intentar registrar un nuevo check-in | El sistema rechaza el check-in por estar dentro de la ventana de 2 horas (RN12) |
| CP07 | Sugerencia de IA respeta ficha de salud | Alumno con `problemas_cardiacos = true` | Solicitar sugerencia de rutina | El sistema no sugiere ninguna rutina marcada como contraindicada para esa condición (RN20) |
| CP08 | Rutina no visible sin aprobación | Existe una sugerencia en estado `pendiente` | Consultar el Panel del Alumno antes de la aprobación | La rutina no aparece en el panel hasta que el entrenador la aprueba (RN21) |
| CP09 | Baja lógica conserva historial | Alumno con pagos e inscripciones registrados | Dar de baja al alumno | El registro pasa a `activo = false`; los pagos e inscripciones previos siguen existiendo y son consultables (RN14, RF14) |
| CP10 | Regeneración de código de acceso | Alumno reporta pérdida del código | El administrador solicita la regeneración | Se genera un código nuevo, distinto al anterior, y el código viejo deja de ser válido |
| CP11 | Configuración de días "por vencer" | Parámetro `dias_aviso_vencimiento` modificado a 10 | Consultar estado de una inscripción a 8 días del vencimiento | El estado se muestra como `por_vencer` (antes hubiera sido `activo` con el valor por defecto de 7) |
| CP12 | Alta de entrenador habilita carga de rutinas | No existe el entrenador en el sistema | Intentar cargar una rutina sin entrenador registrado, luego registrarlo y reintentar | La carga falla sin entrenador registrado (RN24) y se completa correctamente una vez dado de alta |
