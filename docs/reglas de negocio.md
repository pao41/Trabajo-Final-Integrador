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
- **RN09**— Una inscripción se considera "por vencer" cuando faltan menos de 7 días para su fecha de vencimiento. Este valor es configurable desde el Módulo de Configuración.

## Asistencia

- **RN09** — El registro de asistencia se realiza mediante check-in manual desde el mostrador, no automatizado.
- **RN10** — El check-in queda asociado a fecha y hora del momento del registro.
- **RN11** — Un alumno no puede registrar dos check-ins dentro de la misma franja horaria.

## Roles y acceso

- **RN11** — El sistema no distingue roles rígidos de "dueño" y "recepcionista": cualquier usuario administrador/staff puede operar todas las funciones administrativas.
- **RN12** — El alumno accede a su panel de autoconsulta mediante un código simple o su DNI, sin sistema de contraseñas en esta versión.
- **RN13** — El panel de autoconsulta es de solo lectura: el alumno puede ver su información, pero no puede modificar datos de pagos, planes ni asistencia.

## Rutinas y Asistente de IA

- **RN14** — El asistente de IA no genera ejercicios ni rutinas nuevas: únicamente filtra y sugiere entre un banco de rutinas predefinido, cargado y mantenido por el entrenador.
- **RN15** — Cada rutina del banco indica explícitamente qué condiciones de salud la excluyen (por ejemplo, no apta para alumnos con problemas cardíacos declarados).
- **RN16** — El asistente solo puede sugerir rutinas compatibles con la ficha de salud declarada por el alumno.
- **RN17** — Ninguna rutina sugerida llega al alumno de forma automática: debe quedar en estado `pendiente` y ser aprobada explícitamente por un entrenador antes de estar disponible.
- **RN18** — El alcance del asistente se limita a ejercicios de calentamiento, movilidad articular y vuelta a la calma. No incluye rutinas de fuerza ni de alta intensidad.
- **RN19** — Toda rutina mostrada al alumno debe incluir la aclaración de que es una guía orientativa y no reemplaza la supervisión presencial del entrenador ni una evaluación médica profesional.

## Datos y responsabilidad profesional

- **RN20** — El sistema no realiza diagnósticos médicos ni evaluaciones de aptitud física; la ficha de salud es una declaración del propio alumno, sin validación clínica.
- **RN21** — El sistema no almacena datos de tarjetas de pago; el método de pago se registra solo como categoría (efectivo, transferencia, débito, crédito).

