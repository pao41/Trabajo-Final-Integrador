# Endpoints de la API — Sistema de Gestión para Gimnasios

Este documento describe los endpoints de la API REST del sistema, organizados por módulo. Los nombres de los recursos se definen en español y en plural (por ejemplo, /alumnos o /inscripciones), y los datos se intercambian en formato JSON. La documentación interactiva de la API se genera automáticamente y puede consultarse en /docs mientras el backend está en ejecución.

El acceso a cada endpoint depende del perfil del usuario, conforme a la matriz de permisos de [`seguridad_y_permisos.md`](./seguridad_y_permisos.md). La sesión del personal se mantiene mediante una cookie HttpOnly, por lo que no es necesario enviar credenciales en cada petición.

La columna "Estado" indica que el endpoint ya se encuentra disponible.

## Estado del sistema y sesión (módulo 11)

| Método y ruta | Descripción | Acceso | Estado |
|---|---|---|---|
| `GET /salud` | Verifica que el backend y la base de datos responden | Público | Disponible |
| `POST /auth/token` | Inicio de sesión del personal; deja la cookie de sesión | Público | Disponible |
| `POST /auth/logout` | Cierra la sesión | Sesión iniciada | Disponible |
| `GET /auth/me` | Devuelve el usuario de la sesión actual | Sesión iniciada | Disponible |

## Usuarios (módulo 11)

| Método y ruta | Descripción | Acceso | Estado |
|---|---|---|---|
| `GET /usuarios` | Lista los usuarios del personal | Administrador | Disponible |
| `POST /usuarios` | Crea un usuario con su perfil (administrador o entrenador); el perfil entrenador se vincula a un entrenador que todavía no tenga usuario | Administrador | Disponible |
| `PATCH /usuarios/{id}/desactivar` | Desactiva un usuario | Administrador | Disponible |
| `PATCH /usuarios/{id}/activar` | Reactiva un usuario | Administrador | Disponible |
| `PUT /usuarios/{id}/password` | Restablece la contraseña | Administrador | Disponible |

## Entrenadores (módulo 10)

Cada entrenador se da de alta con su nombre y un contacto opcional. Para que pueda entrar al sistema, el administrador le crea un usuario con perfil entrenador desde Usuarios. Cada entrenador tiene un solo usuario.

| Método y ruta | Descripción | Acceso | Estado |
|---|---|---|---|
| `GET /entrenadores` | Lista los entrenadores ordenados por nombre | Administrador | Disponible |
| `POST /entrenadores` | Da de alta un entrenador | Administrador | Disponible |
| `PUT /entrenadores/{id}` | Edita el nombre y el contacto de un entrenador | Administrador | Disponible |

## Rutinas (módulo 7)

Banco de rutinas de calentamiento, movilidad y vuelta a la calma. Cada rutina indica sus contraindicaciones y queda asociada al entrenador que la cargó. Solo el entrenador carga y edita rutinas; el administrador las consulta.

| Método y ruta | Descripción | Acceso | Estado |
|---|---|---|---|
| `GET /rutinas` | Lista las rutinas del banco | Administrador y entrenador | Disponible |
| `POST /rutinas` | Carga una rutina a nombre del entrenador de la sesión | Entrenador | Disponible |
| `PUT /rutinas/{id}` | Edita una rutina; conserva al entrenador que la cargó | Entrenador | Disponible |

## Asistente de IA (módulo 8)

El asistente no genera ejercicios: filtra el banco de rutinas según la ficha de salud del alumno y deja una sugerencia en estado pendiente. Una rutina se descarta si sus contraindicaciones mencionan los problemas cardíacos o alguna de las lesiones de la ficha, y no se vuelve a sugerir una rutina que el alumno ya tuvo sugerida. Solo se puede tener una sugerencia pendiente a la vez. La rutina llega al alumno únicamente si un entrenador la aprueba.

| Método y ruta | Descripción | Acceso | Estado |
|---|---|---|---|
| `POST /sugerencias` | El alumno pide una sugerencia; queda pendiente | Alumno | Disponible |
| `GET /sugerencias` | Lista las sugerencias; con `?estado=pendiente`, `aprobada` o `rechazada` filtra por estado | Administrador y entrenador | Disponible |
| `PATCH /sugerencias/{id}/aprobar` | Aprueba una sugerencia pendiente a nombre del entrenador | Entrenador | Disponible |
| `PATCH /sugerencias/{id}/rechazar` | Rechaza una sugerencia pendiente a nombre del entrenador | Entrenador | Disponible |

## Panel del Alumno (módulo 6)

El alumno entra con su DNI y su código de acceso, sin contraseña. Su sesión usa una cookie HttpOnly propia, distinta de la del personal, y dura 60 minutos. Las rutinas aprobadas por el entrenador siempre se muestran con la aclaración de que son una guía orientativa.

| Método y ruta | Descripción | Acceso | Estado |
|---|---|---|---|
| `POST /panel-alumno/acceso` | Valida DNI y código y deja la cookie de sesión del alumno; tras 5 intentos fallidos seguidos bloquea el acceso 15 minutos | Público | Disponible |
| `POST /panel-alumno/salir` | Cierra la sesión del alumno | Público | Disponible |
| `GET /panel-alumno/resumen` | Estado de la cuota, clases restantes y checklist de la semana | Alumno | Disponible |
| `GET /panel-alumno/asistencias` | Historial de ingresos del propio alumno | Alumno | Disponible |
| `GET /panel-alumno/rutinas` | Rutinas aprobadas por el entrenador, con la aclaración obligatoria | Alumno | Disponible |

## Alumnos (módulo 1)

Los alumnos no se eliminan: la baja es lógica y conserva todo su historial. Al darlos de alta el sistema genera su código de acceso, que se muestra una sola vez. La ficha de salud también la puede consultar, sin modificarla, el entrenador.

| Método y ruta | Descripción | Acceso | Estado |
|---|---|---|---|
| `GET /alumnos` | Lista los alumnos; con `buscar` filtra por nombre o DNI | Administrador | Disponible |
| `POST /alumnos` | Da de alta un alumno y genera su código de acceso; el DNI no se repite | Administrador | Disponible |
| `GET /alumnos/{id}` | Datos de un alumno | Administrador | Disponible |
| `PUT /alumnos/{id}` | Modifica nombre, DNI y contacto | Administrador | Disponible |
| `PATCH /alumnos/{id}/desactivar` | Baja lógica del alumno | Administrador | Disponible |
| `PATCH /alumnos/{id}/activar` | Reactiva al alumno | Administrador | Disponible |
| `POST /alumnos/{id}/codigo-acceso` | Genera un código de acceso nuevo; el anterior deja de servir | Administrador | Disponible |
| `GET /alumnos/{id}/ficha-salud` | Consulta la ficha de salud | Administrador y entrenador | Disponible |
| `PUT /alumnos/{id}/ficha-salud` | Carga o modifica la ficha de salud (una por alumno) | Administrador | Disponible |
| `GET /alumnos/{id}/meta` | Meta semanal de asistencias (3 por defecto) | Administrador | Disponible |
| `PUT /alumnos/{id}/meta` | Modifica la meta semanal de asistencias | Administrador | Disponible |

## Demás módulos

| Módulo | Endpoints | Acceso | Estado |
|---|---|---|---|
| 2. Planes e inscripciones | `GET/POST/PUT /planes`, `POST /inscripciones`, `GET /inscripciones` | Administrador | Próximamente |
| 3. Pagos | `POST /pagos`, `GET /pagos` (historial por alumno) | Administrador | Próximamente |
| 4. Asistencia | `POST /asistencias` (check-in), `GET /asistencias` | Administrador | Próximamente |
| 5. Dashboard | `GET /dashboard` | Administrador | Próximamente |
| 9. Configuración | `GET/PUT /configuracion` | Administrador | Próximamente |

Las rutas de los módulos próximos son el diseño inicial y pueden ajustarse durante la implementación.

