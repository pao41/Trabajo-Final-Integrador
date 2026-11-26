# Funcionalidades Futuras y Escalabilidad — Sistema de Gestión para Gimnasios

Posibles mejoras con las que el sistema podría crecer a medida que el gimnasio aumente su cantidad de alumnos y de servicios. Son ideas de evolución, no compromisos de desarrollo.

---

## Notificaciones automáticas de cuota
El sistema podría enviar avisos por email o por WhatsApp cuando la cuota de un alumno esté por vencer o ya haya vencido, aprovechando los días de anticipación que hoy se configuran para el estado "por vencer". De esta manera el personal ya no tendría que avisar uno por uno, se reduciría la morosidad y el alumno recibiría el recordatorio a tiempo.

## Check-in por código QR
Cada alumno podría registrar su ingreso escaneando un código personal, en lugar de que el personal lo busque y lo marque manualmente en el mostrador. Se agilizaría el ingreso en los horarios de mayor concurrencia, se evitarían errores de carga y el personal podría dedicar ese tiempo a atender a los alumnos.

## Pagos online
El alumno podría abonar su cuota desde la web mediante una pasarela de pago, y el sistema registraría el pago y renovaría la inscripción de forma automática. Esto evitaría que el alumno tenga que acercarse al gimnasio solo para pagar y reduciría la carga administrativa de registrar cada cobro.

## Análisis de asistencia y horas pico
A partir de las asistencias que el sistema ya registra, se podrían mostrar gráficos con los días y los horarios de mayor concurrencia a lo largo de la semana. El gimnasio podría usar esa información para organizar los turnos de los entrenadores, programar las clases en los mejores horarios y detectar a los alumnos que dejaron de asistir.

## Mejoras del asistente de IA
Hoy el asistente guía al alumno con dos preguntas (cómo se siente y qué quiere hacer), elige una rutina compatible con su ficha de salud y explica el motivo, pero la sugerencia queda pendiente hasta que un entrenador la aprueba. Como mejoras futuras se proponen:

* **Entrega inmediata con banco validado:** si el entrenador revisa de antemano el banco de rutinas y marca cuáles pueden entregarse sin revisión individual, el alumno podría recibir la rutina al instante, y el entrenador podría revisarla después y retirarla si no la considera adecuada. Esto cambiaría la regla RN21 y requeriría confirmarlo con el tutor y con el gimnasio.
* **Conversación libre:** permitir que el alumno escriba su consulta en lugar de elegir opciones, manteniendo el filtro por ficha de salud y la restricción a rutinas del banco.
* **Más preguntas y mejores criterios:** considerar, por ejemplo, el tiempo disponible o el objetivo del alumno, y ampliar el banco con más ejercicios.
* **Historial de consultas:** que el alumno y el entrenador puedan ver las consultas anteriores y las explicaciones recibidas.

En todos los casos se mantendría el alcance limitado a calentamiento, movilidad y vuelta a la calma, y la supervisión del entrenador, previa o posterior a la entrega.

## Aplicación móvil
El Panel del Alumno podría ofrecerse como una aplicación para el celular o como una web instalable, con avisos en el teléfono. El alumno podría consultar su estado de cuota, su asistencia y sus rutinas aprobadas desde cualquier lugar, sin depender de una computadora.

## Varias sedes y varios gimnasios
El sistema podría admitir un gimnasio con varias sucursales, con alumnos, asistencia y facturación separados por sede, o bien atender a distintos gimnasios dentro de un mismo sistema, con sus datos aislados entre sí. Esto permitiría acompañar el crecimiento del negocio y ofrecer el sistema a otros establecimientos sin instalar una versión distinta para cada uno.

## Mayor volumen de datos y usuarios
A medida que se acumulen alumnos, pagos y asistencias, se podrían paginar los listados, optimizar las consultas del dashboard y aumentar la capacidad del backend y de la base de datos, aprovechando que cada capa se despliega por separado. El objetivo sería mantener tiempos de respuesta cortos aunque aumente la cantidad de usuarios simultáneos.