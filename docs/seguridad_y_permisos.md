# Seguridad y Permisos — Sistema de Gestión para Gimnasios

Este documento detalla cómo se protege el acceso al sistema (Panel del Alumno y Panel Administrador), qué perfiles existen y qué puede hacer cada uno. Complementa la sección de Seguridad de [`arquitectura.md`](./arquitectura.md).

## 1. Datos a proteger

| Tipo de dato | Dónde se guarda | Nivel de protección |
|---|---|---|
| Datos personales (nombre, DNI, contacto) | `alumnos` | Acceso solo para personal autenticado |
| Datos de salud declarados | `ficha_salud` | Datos sensibles: acceso restringido por perfil (RN39), nunca visibles en el Panel del Alumno |
| Credenciales de alumnos y personal | `alumnos.codigo_acceso_hash`, `usuarios.password_hash` | Se guardan solo como hash, nunca en texto plano (RN33, RN37) |
| Datos de pago | `pagos` | Solo el método como categoría; no se guardan datos de tarjetas (RN27) |

## 2. Acceso del alumno (Panel del Alumno)

El acceso por DNI solo no es seguro, porque el DNI no es un dato secreto. Por eso el alumno debe ingresar **DNI y código de acceso** (RN16).

| Mecanismo | Qué evita | Regla |
|---|---|---|
| Se exigen DNI **y** código de acceso | Que alguien entre conociendo solo el DNI de otra persona | RN16 |
| El código lo genera el sistema de forma aleatoria (8 caracteres alfanuméricos) y no se deriva del DNI | Códigos fáciles de adivinar | RN37 |
| El código se guarda como hash y se muestra al personal una sola vez, al generarlo o regenerarlo | Que alguien con acceso a la base lea los códigos | RN37 |
| Después de 5 intentos fallidos seguidos se bloquea el acceso durante 15 minutos | Ataques de prueba y error | RN38 |
| El mensaje de error es genérico ("datos incorrectos"), sin indicar si falló el DNI o el código | Descubrir qué DNI están registrados | RN38 |
| Panel de solo lectura que muestra únicamente datos del propio alumno | Que un alumno vea o modifique datos de otros | RN17 |
| La ficha de salud no se muestra en el Panel del Alumno | Exposición de datos sensibles | RN39 |
| Al regenerar el código, el anterior deja de ser válido | Uso de un código perdido o robado | RF15, RN37 |
| La sesión es temporal (token con vencimiento) y todo viaja por HTTPS | Sesiones abiertas indefinidamente, interceptación y robo del token por scripts maliciosos | RNF09 |


## 3. Acceso del personal (Panel Administrador)

El personal ingresa con **usuario y contraseña** (RF21, RN33).

- Las contraseñas se guardan con hash (por ejemplo, bcrypt), nunca en texto plano.
- Se aplica el mismo bloqueo temporal por intentos fallidos que en el acceso del alumno (RN38).
- Los usuarios no se borran: se desactivan (`usuarios.activo = false`), para conservar el historial de quién realizó cada acción.
- El administrador crea los usuarios con su perfil, los desactiva y restablece contraseñas (RF23). No hay autoregistro.
- El backend valida el perfil del usuario en **cada** petición; ocultar un botón en el frontend no alcanza como control.

## 4. Perfiles y matriz de permisos

El sistema tiene dos perfiles y cada usuario tiene uno solo (RN34). Se mantienen pocos perfiles a propósito: es un gimnasio chico, donde el dueño o responsable atiende el mostrador y el entrenador solo trabaja con las rutinas.

| Perfil | Quién es | Vinculación |
|---|---|---|
| Administrador | Dueño o responsable del gimnasio, que también atiende el mostrador | Ninguna |
| Entrenador | Profesor que carga y valida rutinas | Se vincula con un registro de `entrenadores` (RN35) |

Si el dueño también entrena, se le crean dos usuarios, uno por perfil.

**Matriz de permisos** (✔ permitido, — no permitido):

| Función | Administrador | Entrenador |
|---|:---:|:---:|
| Alta y edición de alumnos | ✔ | — |
| **Baja lógica de alumnos** | ✔ | — |
| **Regenerar el código de acceso de un alumno** | ✔ | — |
| Cargar y editar la ficha de salud | ✔ | — |
| Consultar la ficha de salud | ✔ | ✔ |
| **Crear y editar planes y precios** | ✔ | — |
| Inscribir alumnos y renovar | ✔ | — |
| Registrar pagos | ✔ | — |
| Registrar asistencia (check-in) | ✔ | — |
| Listado de alumnos por estado | ✔ | — |
| Configurar la meta semanal de un alumno | ✔ | — |
| **Dashboard (facturación e ingresos)** | ✔ | — |
| **Configuración general del sistema** | ✔ | — |
| **Gestionar entrenadores** | ✔ | — |
| **Gestionar usuarios** | ✔ | — |
| Cargar y editar rutinas del banco | — | ✔ |
| Aprobar o rechazar sugerencias del Asistente de IA | — | ✔ |
| Consultar rutinas y sugerencias | ✔ (lectura) | ✔ |

Las funciones en **negrita** son las acciones sensibles. Quedan a cargo del administrador, por lo que el entrenador no puede gestionar entrenadores, usuarios, configuración ni ver la facturación (RN36). La carga de rutinas y la aprobación de sugerencias son exclusivas del entrenador porque quedan registradas a su nombre (RN24, RN35).

## 5. Acciones sensibles y registro

Las acciones sensibles se registran en el log del backend con usuario, acción, fecha y hora (RN40). El detalle del registro está en [`contingencia_auditoria_recuperacion.md`](./contingencia_auditoria_recuperacion.md).

| Acción sensible | Perfil habilitado |
|---|---|
| Baja lógica de un alumno | Administrador |
| Regeneración de código de acceso | Administrador |
| Alta o edición de entrenadores (RF17); su acceso se corta desactivando su usuario | Administrador |
| Alta o desactivación de usuarios y restablecimiento de contraseñas | Administrador |
| Cambios en configuración, planes y precios | Administrador |
| Aprobación o rechazo de una sugerencia de rutina | Entrenador |

## 6. Protección de datos personales y de salud

Se toman como marco los principios de la Ley 25.326 de Protección de Datos Personales, que considera sensibles a los datos de salud:

- **Finalidad:** la ficha de salud se usa solo para filtrar rutinas seguras, no para otros fines.
- **Consentimiento:** el alumno declara los datos de forma voluntaria al inscribirse.
- **Minimización:** se piden solo los datos necesarios (condición cardíaca, lesiones, observaciones).
- **Confidencialidad:** acceso limitado por perfil y comunicación cifrada con HTTPS.
- **Registros sin datos sensibles:** el log del backend no incluye contraseñas, códigos de acceso ni datos de salud.

## 7. Limitaciones del MVP y mejoras futuras

- No se incluye doble factor de autenticación ni recuperación de contraseña por email: el administrador restablece las credenciales.
- El cifrado de los datos en reposo depende del proveedor de hosting de la base de datos.
- La recuperación de contraseña autoservicio y las notificaciones por email quedan como mejora futura.
