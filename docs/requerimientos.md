# Requerimientos Funcionales y No Funcionales — Sistema de Gestión para Gimnasios

## Paneles del sistema

El sistema se organiza en dos paneles diferenciados, según el actor que los utiliza:

- **Panel Administrador:** utilizado por el personal del gimnasio, que debe iniciar sesión con usuario y contraseña. Concentra la gestión de alumnos, planes, inscripciones, pagos, asistencia, el dashboard de facturación, la configuración, la gestión de usuarios y entrenadores, y la aprobación de rutinas sugeridas por el asistente de IA. Cada usuario tiene un perfil (administrador o entrenador) que determina qué funciones tiene habilitadas.
- **Panel del Alumno:** de solo lectura, accesible ingresando DNI y código de acceso. Permite al alumno consultar su estado de cuota, su historial de asistencia, su checklist personal, y las rutinas ya aprobadas por el entrenador.

## Requerimientos Funcionales (RF)

| # | Requerimiento |
|---|---|
| RF01 | El sistema debe permitir registrar, editar y dar de baja (lógica) alumnos (nombre, DNI, contacto), generando un código de acceso para el Panel del Alumno. |
| RF02 | El sistema debe permitir registrar la ficha de salud básica de cada alumno (problemas cardíacos, lesiones, observaciones). |
| RF03 | El sistema debe permitir crear y editar planes (nombre, duración, precio y tipo: por tiempo o por clases; en los planes por clases, también la cantidad de clases incluidas). |
| RF04 | El sistema debe permitir inscribir a un alumno en un plan, calculando automáticamente la fecha de vencimiento. |
| RF05 | El sistema debe actualizar automáticamente el estado de cada inscripción (activo / por vencer / vencido) según la fecha actual. |
| RF06 | El sistema debe permitir registrar pagos asociados a una inscripción, indicando fecha, monto y método de pago. |
| RF07 | El sistema debe permitir registrar el ingreso diario de un alumno (check-in manual desde el mostrador), asociándolo a su inscripción vigente. |
| RF08 | El sistema debe mostrar un dashboard con facturación total del mes y desglose por método de pago. |
| RF09 | El sistema debe mostrar el listado de alumnos filtrado por estado (activo / por vencer / vencido). |
| RF10 | El sistema debe ofrecer un panel de autoconsulta para que el alumno vea su estado de cuota e historial de asistencia, accediendo con su DNI y su código de acceso. |
| RF11 | El sistema debe permitir cargar un banco de rutinas de calentamiento, movilidad y vuelta a la calma, indicando contraindicaciones de salud para cada una. |
| RF12 | El sistema debe sugerir rutinas al alumno filtrando el banco de rutinas según su ficha de salud, sin generar ejercicios nuevos. |
| RF13 | Toda rutina sugerida debe quedar en estado "pendiente" hasta ser aprobada por un entrenador antes de estar disponible para el alumno. |
| RF14 | El sistema debe conservar el historial completo de pagos e inscripciones de cada alumno, sin eliminarlo ante bajas o cambios de plan. |
| RF15 | El sistema debe permitir al personal del gimnasio regenerar el código de acceso de un alumno desde el Panel Administrador, en caso de pérdida u olvido; el código anterior deja de ser válido. |
| RF16 | El sistema debe permitir configurar parámetros generales: datos del gimnasio, días de anticipación para el estado "por vencer", y métodos de pago habilitados. |
| RF17 | El sistema debe permitir al administrador dar de alta y editar entrenadores. |
| RF18 | El sistema debe asociar cada rutina cargada y cada rutina aprobada al entrenador que realizó la acción. |
| RF19 | El sistema debe permitir configurar una meta semanal de asistencias por alumno, utilizada para calcular el checklist del Panel del Alumno. |
| RF20 | El sistema debe gestionar el saldo de clases de las inscripciones por clases: inicializarlo al inscribir, descontar una clase por cada ingreso registrado y no registrar ingresos cuando el saldo sea cero (ver [`planes_por_clases.md`](./planes_por_clases.md)). |
| RF21 | El sistema debe requerir usuario y contraseña al personal del gimnasio para acceder al Panel Administrador. |
| RF22 | El sistema debe restringir las funciones del Panel Administrador según el perfil del usuario (administrador o entrenador), conforme a la matriz de permisos. |
| RF23 | El sistema debe permitir al administrador crear usuarios del personal con su perfil, desactivarlos y restablecer sus contraseñas. |


## Requerimientos No Funcionales (RNF)

| # | Requerimiento |
|---|---|
| RNF01 | **Usabilidad:** la interfaz debe ser simple e intuitiva, utilizable por personal sin conocimientos técnicos, sin requerir capacitación extensa. |
| RNF02 | **Rendimiento:** las operaciones habituales (registrar pago, marcar asistencia, consultar dashboard) deben responder en tiempos cortos, sin demoras perceptibles para el usuario. |
| RNF03 | **Portabilidad/Accesibilidad:** el sistema debe ser accesible desde cualquier navegador web moderno, sin necesidad de instalación, y con diseño responsive para distintos tamaños de pantalla. |
| RNF04 | **Disponibilidad:** el sistema debe estar desplegado en servicios de hosting en la nube, accesible de forma continua. |
| RNF05 | **Mantenibilidad:** el código debe organizarse en capas separadas (frontend, backend, base de datos) para facilitar su mantenimiento y evolución futura. |
| RNF06 | **Escalabilidad:** la arquitectura relacional debe soportar el crecimiento en cantidad de alumnos y registros sin requerir cambios estructurales mayores. |
| RNF07 | **Seguridad de acceso:** el alumno accede con DNI y código de acceso y el personal con usuario y contraseña. Las credenciales se almacenan cifradas (hash) y los intentos fallidos consecutivos provocan un bloqueo temporal. |
| RNF08 | **Consistencia de datos:** el sistema debe preservar la consistencia de los datos entre entidades relacionadas (alumno, plan, inscripción, pago, asistencia), evitando registros huérfanos o inconsistentes. |
| RNF09 | **Protección de datos personales y de salud:** las comunicaciones deben realizarse por HTTPS, las sesiones deben ser temporales y el acceso a los datos personales y de salud debe limitarse según el perfil del usuario, tomando como marco los principios de la Ley 25.326. |
| RNF10 | **Auditoría:** las acciones sensibles deben quedar registradas (usuario, acción, fecha y hora) y las operaciones históricas no deben eliminarse físicamente. |
| RNF11 | **Recuperación:** deben existir copias de respaldo periódicas de la base de datos y un procedimiento de restauración, con objetivo de pérdida máxima de datos de 24 horas y recuperación dentro de una jornada laboral. |
| RNF12 | **Continuidad operativa:** ante la indisponibilidad del sistema, el gimnasio debe poder seguir operando con un procedimiento manual de contingencia y cargar luego la información. |