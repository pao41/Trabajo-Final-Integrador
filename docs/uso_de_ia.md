# Uso de herramientas de Inteligencia Artificial

Durante el desarrollo del Trabajo Final Integrador se utilizaron herramientas de Inteligencia Artificial generativa como apoyo complementario en distintas etapas del proyecto.

Su utilización estuvo orientada principalmente a facilitar la comprensión de conceptos técnicos, resolver dudas puntuales y acompañar el proceso de desarrollo, sin reemplazar el análisis, las decisiones ni la implementación realizada por los integrantes del equipo.

Los principales usos fueron:

* Análisis: consultas para aclarar algunos requerimientos y resolver dudas sobre aspectos técnicos antes de su implementación.
* Codificación: consultas puntuales sobre sintaxis, estructuras de programación y funcionamiento de determinadas herramientas utilizadas.
* Depuración: apoyo para interpretar mensajes de error y analizar posibles soluciones durante el desarrollo.
* Documentación técnica: asistencia en la revisión de la documentación elaborada por los integrantes del equipo y consultas puntuales sobre su contenido técnico.

## Criterios de utilización

Las respuestas y sugerencias proporcionadas por estas herramientas fueron consideradas como referencias de consulta. Cada propuesta fue revisada por los integrantes del equipo, contrastada con los conocimientos adquiridos durante la formación académica y adaptada a las necesidades del proyecto antes de su utilización.

La selección de tecnologías, las decisiones de diseño, la implementación de las funcionalidades y la validación del funcionamiento del sistema estuvieron a cargo de los integrantes del equipo.

La Inteligencia Artificial se utilizó, por lo tanto, como una herramienta de asistencia al aprendizaje y al desarrollo, manteniendo la responsabilidad sobre el código, las decisiones técnicas y los resultados obtenidos.

## Inteligencia Artificial dentro del sistema

Además de su uso durante el desarrollo, el sistema incorpora un asistente de rutinas para el alumno que utiliza un servicio externo de Inteligencia Artificial (Gemini, de Google).

**Qué hace la IA:** entre las rutinas que el sistema ya filtró como compatibles con la ficha de salud del alumno, elige una según cómo se siente y qué quiere hacer, y redacta una explicación breve.

**Qué no hace la IA:** no decide qué rutinas son seguras, no crea ejercicios nuevos y no aprueba nada. El filtro por ficha de salud lo realiza el sistema con reglas fijas (RN20) y toda sugerencia queda pendiente hasta que un entrenador la aprueba (RN21).

**Datos que recibe:** solo las condiciones de salud declaradas, cómo se siente el alumno, el tipo de rutina elegido y el nombre y la descripción de las rutinas candidatas. No recibe nombre, DNI ni datos de contacto (RN43). La clave del servicio se guarda como variable de entorno y no forma parte del código.

**Si la IA no está disponible:** el sistema sigue funcionando y sugiere la primera rutina compatible, sin explicación.

**Nota sobre la privacidad:** las condiciones de uso del plan gratuito de Gemini pueden permitir que Google utilice los datos enviados para mejorar sus productos. Para un uso real con alumnos, se recomienda un plan pago o la revisión de esas condiciones antes de ponerlo en producción.