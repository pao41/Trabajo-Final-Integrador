# Reglas de Negocio — Sistema de Gestión para Gimnasios

## Planes, inscripciones y pagos

- **RN01** — El estado de una inscripción puede ser `activo`, `por_vencer` o `vencido`. No es un valor binario.
- **RN02** — La fecha de vencimiento de una inscripción se calcula como: `fecha_pago + duración_del_plan`.
- **RN03** — Si el alumno paga antes de la fecha de vencimiento actual, la duración del nuevo pago se suma al vencimiento vigente (no se pierde el tiempo restante).
- **RN04** — Si el alumno paga después de vencida su inscripción, el plan se reactiva desde la fecha del nuevo pago. No se recupera ni se descuenta el tiempo que estuvo vencido.
- **RN05** — El sistema no contempla pagos parciales en esta versión: cada pago corresponde al valor completo del período contratado.
- **RN06** — El cambio de plan de un alumno se aplica a partir de la próxima renovación; no se hacen cálculos proporcionales del plan anterior a mitad de período.
- **RN07** — El sistema no gestiona reembolsos ni cancelaciones de pagos ya registrados.
- **RN08** — El método de pago (efectivo, transferencia, débito, crédito) es un dato informativo para el dashboard; el sistema no integra pasarelas de pago reales.
- **RN09** — Una inscripción se considera "por vencer" cuando faltan menos de 7 días para su fecha de vencimiento. Este valor es configurable desde el Módulo de Configuración.

## Asistencia

- **RN10** — El registro de asistencia se realiza mediante check-in manual desde el mostrador, no automatizado.
- **RN11** — El check-in queda asociado a fecha y hora del momento del registro.
- **RN12** — Un alumno no puede registrar dos check-ins dentro de una ventana de 2 horas desde su check-in anterior.

## Alumnos
- **RN13** — No pueden existir dos alumnos con el mismo DNI; el sistema debe impedir el alta duplicada.
- **RN14** — La baja de un alumno es lógica: el registro no se elimina de la base de datos, sino que se marca como inactivo, preservando su historial de pagos y asistencia.

## Roles y acceso

- **RN15** — El sistema distingue dos perfiles de personal (administrador y entrenador). Cada perfil accede solo a las funciones habilitadas en la matriz de permisos de [`seguridad_y_permisos.md`](./seguridad_y_permisos.md)
- **RN16** — El alumno accede a su panel de autoconsulta ingresando su DNI y su código de acceso; ambos datos son obligatorios. El DNI solo no habilita el acceso.
- **RN17** — El panel de autoconsulta es de solo lectura y muestra únicamente los datos del propio alumno: no puede modificar datos de pagos, planes ni asistencia, ni ver información de otros alumnos.

## Rutinas y Asistente de IA

- **RN18** — El asistente de IA no genera ejercicios ni rutinas nuevas: únicamente filtra y sugiere entre un banco de rutinas predefinido, cargado y mantenido por el entrenador.
- **RN19** — Cada rutina del banco indica explícitamente qué condiciones de salud la excluyen (por ejemplo, no apta para alumnos con problemas cardíacos declarados).
- **RN20** — El asistente solo puede sugerir rutinas compatibles con la ficha de salud declarada por el alumno.
- **RN21** — Ninguna rutina sugerida llega al alumno de forma automática: debe quedar en estado `pendiente` y ser aprobada explícitamente por un entrenador antes de estar disponible.
- **RN22** — El alcance del asistente se limita a ejercicios de calentamiento, movilidad articular y vuelta a la calma. No incluye rutinas de fuerza ni de alta intensidad.
- **RN23** — Toda rutina mostrada al alumno debe incluir la aclaración de que es una guía orientativa y no reemplaza la supervisión presencial del entrenador ni una evaluación médica profesional.

## Entrenadores

- **RN24** — Un entrenador debe existir registrado en el sistema antes de poder cargar rutinas o aprobar sugerencias generadas por el Asistente de IA.

## Checklist y metas personales
- **RN25** — Cada alumno tiene una meta semanal de asistencias configurable (valor por defecto: 3 por semana). El checklist del Panel del Alumno se calcula comparando las asistencias registradas en la semana en curso contra esta meta.

## Datos y responsabilidad profesional

- **RN26** — El sistema no realiza diagnósticos médicos ni evaluaciones de aptitud física; la ficha de salud es una declaración del propio alumno, sin validación clínica.
- **RN27** — El sistema no almacena datos de tarjetas de pago; el método de pago se registra solo como categoría (efectivo, transferencia, débito, crédito).

## Auditoría y trazabilidad operativa

- **RN28** — Todo registro de pago, inscripción, asistencia, carga de rutina y validación de sugerencias del Asistente de IA conserva su fecha de ejecución y el entrenador responsable cuando corresponda, sin permitir el borrado físico de operaciones históricas.

## Planes por cantidad de clases

- **RN29** — Un plan de tipo `clases` define una cantidad de clases (`cantidad_clases`) y una vigencia en días (`duracion_dias`). Un plan de tipo `tiempo` no define cantidad de clases.
- **RN30** — Al inscribir a un alumno en un plan por clases, su saldo (`clases_restantes`) se inicializa con la cantidad de clases del plan. Cada ingreso registrado descuenta una (1) clase del saldo, en la misma operación que guarda la asistencia. El saldo nunca puede ser negativo.
- **RN31** — Una inscripción por clases pasa a `vencido` cuando su saldo llega a cero o cuando vence su vigencia, lo que ocurra primero. Las clases no utilizadas al vencer la vigencia se pierden.
- **RN32** — Si el saldo es cero, el sistema no registra el ingreso y avisa al personal que corresponde renovar. Al renovar con un nuevo pago se aplica RN03 si la vigencia todavía no venció (el saldo se suma a las clases restantes y la vigencia se extiende) o RN04 si ya venció (el saldo se reinicia con la cantidad de clases del plan). El criterio es la fecha de vencimiento, no el estado.

## Seguridad, usuarios y permisos

- **RN33** — El personal accede al Panel Administrador con usuario y contraseña. Las contraseñas se almacenan cifradas (hash) y nunca en texto plano.
- **RN34** — Cada usuario del personal tiene un único perfil (administrador o entrenador) y solo puede ejecutar las funciones habilitadas para ese perfil. Los usuarios no se eliminan: se desactivan.
- **RN35** — Un usuario con perfil entrenador queda vinculado a un registro de entrenadores. La carga de rutinas y la validación de sugerencias se registran a nombre de ese entrenador (ver RN24).
- **RN36** — El perfil administrador tiene a su cargo toda la gestión del gimnasio: alumnos (incluida la baja lógica), planes y precios, inscripciones, pagos, asistencia, dashboard, configuración, entrenadores y usuarios. El perfil entrenador solo puede cargar rutinas, aprobar o rechazar sugerencias y consultar fichas de salud y rutinas.
- **RN37** — El código de acceso del alumno lo genera el sistema de forma aleatoria y no se deriva del DNI. Se almacena cifrado (hash) y se muestra al personal una única vez, al generarlo o regenerarlo. Al regenerarlo, el código anterior deja de ser válido.
- **RN38** — Después de 5 intentos fallidos consecutivos de acceso (alumno o personal) el sistema bloquea nuevos intentos durante 15 minutos. Los mensajes de error son genéricos y no indican qué dato falló.
- **RN39** — La ficha de salud solo puede ser consultada por personal autenticado según su perfil (administrador y entrenador). Nunca se muestra en el Panel del Alumno.
- **RN40** — Las acciones sensibles (baja de alumnos, regeneración de códigos, gestión de entrenadores y usuarios, cambios de configuración, planes y precios, y aprobación o rechazo de rutinas) se registran en el log del backend con usuario, acción, fecha y hora. El registro no incluye contraseñas, códigos de acceso ni datos de salud.

## Contingencia y recuperación

- **RN41** — Ante la indisponibilidad del sistema, el personal registra ingresos y pagos en una planilla manual de contingencia y los carga al restablecerse el servicio, conservando la fecha y hora reales de cada operación.
- **RN42** — Se realizan copias de respaldo periódicas de la base de datos. El archivo `database/schema.sql` permite reconstruir su estructura ante una pérdida total.