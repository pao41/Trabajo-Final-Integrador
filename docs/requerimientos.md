# Requerimientos Funcionales y No Funcionales — Sistema de Gestión para Gimnasios

## Paneles del sistema

El sistema se organiza en dos paneles diferenciados, según el actor que los utiliza:

- **Panel Administrador:** utilizado por el personal del gimnasio. Concentra la gestión de alumnos, planes, inscripciones, pagos, asistencia, el dashboard de facturación y la aprobación de rutinas sugeridas por el asistente de IA antes de que lleguen al alumno.
- **Panel del Alumno:** de solo lectura, accesible mediante un código simple o DNI. Permite al alumno consultar su estado de cuota, su historial de asistencia, su checklist personal, y las rutinas ya aprobadas por el entrenador.

## Requerimientos Funcionales (RF)

| # | Requerimiento |
|---|---|
| RF01 | El sistema debe permitir registrar, editar y dar de baja alumnos (nombre, DNI, contacto, código de acceso). |
| RF02 | El sistema debe permitir registrar la ficha de salud básica de cada alumno (problemas cardíacos, lesiones, observaciones). |
| RF03 | El sistema debe permitir crear y editar planes (nombre, duración, precio, tipo: por tiempo o por clases). |
| RF04 | El sistema debe permitir inscribir a un alumno en un plan, calculando automáticamente la fecha de vencimiento. |
| RF05 | El sistema debe actualizar automáticamente el estado de cada inscripción (activo / por vencer / vencido) según la fecha actual. |
| RF06 | El sistema debe permitir registrar pagos asociados a una inscripción, indicando fecha, monto y método de pago. |
| RF07 | El sistema debe permitir registrar el ingreso diario de un alumno (check-in manual desde el mostrador). |
| RF08 | El sistema debe mostrar un dashboard con facturación total del mes y desglose por método de pago. |
| RF09 | El sistema debe mostrar el listado de alumnos filtrado por estado (activo / por vencer / vencido). |
| RF10 | El sistema debe ofrecer un panel de autoconsulta para que el alumno vea su estado de cuota e historial de asistencia, accediendo mediante código simple o DNI. |
| RF11 | El sistema debe permitir cargar un banco de rutinas de calentamiento, movilidad y vuelta a la calma, indicando contraindicaciones de salud para cada una. |
| RF12 | El sistema debe sugerir rutinas al alumno filtrando el banco de rutinas según su ficha de salud, sin generar ejercicios nuevos. |
| RF13 | Toda rutina sugerida debe quedar en estado "pendiente" hasta ser aprobada por un entrenador antes de estar disponible para el alumno. |
| RF14 | El sistema debe conservar el historial completo de pagos e inscripciones de cada alumno, sin eliminarlo ante bajas o cambios de plan. |

## Requerimientos No Funcionales (RNF)

| # | Requerimiento |
|---|---|
| RNF01 | **Usabilidad:** la interfaz debe ser simple e intuitiva, utilizable por personal sin conocimientos técnicos, sin requerir capacitación extensa. |
| RNF02 | **Rendimiento:** las operaciones habituales (registrar pago, marcar asistencia, consultar dashboard) deben responder en tiempos cortos, sin demoras perceptibles para el usuario. |
| RNF03 | **Portabilidad/Accesibilidad:** el sistema debe ser accesible desde cualquier navegador web moderno, sin necesidad de instalación, y con diseño responsive para distintos tamaños de pantalla. |
| RNF04 | **Disponibilidad:** el sistema debe estar desplegado en servicios de hosting en la nube, accesible de forma continua. |
| RNF05 | **Mantenibilidad:** el código debe organizarse en capas separadas (frontend, backend, base de datos) para facilitar su mantenimiento y evolución futura. |
| RNF06 | **Escalabilidad:** la arquitectura relacional debe soportar el crecimiento en cantidad de alumnos y registros sin requerir cambios estructurales mayores. |
| RNF07 | **Seguridad de acceso:** el acceso del alumno al panel de autoconsulta no debe requerir el ingreso de datos sensibles más allá de un código simple o DNI, evitando el manejo de contraseñas en esta primera versión. |
| RNF08 | **Integridad de datos:** la base de datos debe garantizar integridad referencial entre entidades relacionadas (alumno, plan, inscripción, pago, asistencia) mediante claves foráneas y restricciones. |
