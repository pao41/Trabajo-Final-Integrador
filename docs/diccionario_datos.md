# Diccionario de Datos — Sistema de Gestión para Gimnasios

Las restricciones de cada columna están definidas en [`/database/schema.sql`](../database/schema.sql). La explicación de cuáles controla la base de datos y cuáles la aplicación está en [`integridad_datos.md`](./integridad_datos.md). Todas las claves foráneas usan `ON DELETE RESTRICT`.

## Tabla: alumnos

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único del alumno | PK |
| nombre | VARCHAR(150) | Nombre completo | NOT NULL |
| dni | VARCHAR(20) | Documento de identidad | NOT NULL, UNIQUE (RN13) |
| contacto | VARCHAR(150) | Teléfono o email de contacto | — |
| codigo_acceso_hash | VARCHAR(255) | Hash del código de acceso al Panel del Alumno; el código en sí no se guarda | NOT NULL |
| activo | BOOLEAN | Indica si el alumno está dado de baja (lógica) | NOT NULL, DEFAULT TRUE (RN14) |
| fecha_alta | DATE | Fecha de registro en el sistema | NOT NULL, DEFAULT hoy |

## Tabla: ficha_salud

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| alumno_id | INTEGER | Alumno al que pertenece | NOT NULL, UNIQUE, FK → alumnos(id) |
| problemas_cardiacos | BOOLEAN | Declaración de problemas cardíacos | NOT NULL, DEFAULT FALSE |
| lesiones | TEXT | Lesiones declaradas | — |
| observaciones | TEXT | Otras observaciones de salud | — |
| fecha_registro | DATE | Fecha de carga de la ficha | NOT NULL, DEFAULT hoy |

## Tabla: planes

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| nombre | VARCHAR(100) | Nombre del plan | NOT NULL, UNIQUE |
| duracion_dias | INTEGER | Duración (vigencia) del plan en días | NOT NULL, CHECK (> 0) |
| precio | NUMERIC(10,2) | Precio del plan | NOT NULL, CHECK (> 0) |
| tipo | VARCHAR(20) | `tiempo` o `clases` | NOT NULL, CHECK |
| cantidad_clases | INTEGER | Clases incluidas en el plan; solo para tipo `clases` | CHECK `chk_plan_clases`: obligatoria y mayor que 0 si el tipo es `clases`, nula si es `tiempo` (RN29) |

## Tabla: inscripciones

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| alumno_id | INTEGER | Alumno inscripto | NOT NULL, FK → alumnos(id) |
| plan_id | INTEGER | Plan contratado | NOT NULL, FK → planes(id) |
| fecha_inicio | DATE | Inicio del período contratado | NOT NULL |
| fecha_vencimiento | DATE | Vencimiento calculado (RN02) | NOT NULL, CHECK (>= fecha_inicio) |
| clases_restantes | INTEGER | Saldo de clases; nulo en planes por tiempo | CHECK (nulo o >= 0) (RN30) |
| estado | VARCHAR(20) | `activo` / `por_vencer` / `vencido` | NOT NULL, CHECK, DEFAULT 'activo' (RN01) |

## Tabla: pagos

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| inscripcion_id | INTEGER | Inscripción asociada | NOT NULL, FK → inscripciones(id) |
| fecha_pago | DATE | Fecha en que se registró el pago | NOT NULL, DEFAULT hoy |
| monto | NUMERIC(10,2) | Monto abonado | NOT NULL, CHECK (> 0) (RN05: siempre valor completo del período) |
| metodo_pago | VARCHAR(20) | `efectivo` / `transferencia` / `debito` / `credito` | NOT NULL, CHECK (RN27) |

## Tabla: asistencias

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| alumno_id | INTEGER | Alumno que registró ingreso | NOT NULL, FK → alumnos(id) |
| inscripcion_id | INTEGER | Inscripción vigente contra la que se registró el ingreso; permite reconstruir el consumo de clases | FK → inscripciones(id) |
| fecha | DATE | Fecha del check-in | NOT NULL, DEFAULT hoy |
| hora | TIME | Hora del check-in | NOT NULL, DEFAULT ahora |

## Tabla: entrenadores

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| nombre | VARCHAR(150) | Nombre del entrenador | NOT NULL |
| contacto | VARCHAR(150) | Teléfono o email | — |
| fecha_alta | DATE | Fecha de alta en el sistema | NOT NULL, DEFAULT hoy |

## Tabla: usuarios

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| nombre_usuario | VARCHAR(50) | Nombre con el que el personal inicia sesión | NOT NULL, UNIQUE |
| password_hash | VARCHAR(255) | Hash de la contraseña; la contraseña no se guarda (RN33) | NOT NULL |
| rol | VARCHAR(20) | `administrador` / `entrenador` | NOT NULL, CHECK (RN34) |
| entrenador_id | INTEGER | Entrenador vinculado; solo para el perfil entrenador | UNIQUE, FK → entrenadores(id), CHECK `chk_usuario_entrenador` (RN35) |
| activo | BOOLEAN | Indica si el usuario puede iniciar sesión (los usuarios no se eliminan) | NOT NULL, DEFAULT TRUE |
| fecha_alta | DATE | Fecha de creación del usuario | NOT NULL, DEFAULT hoy |

## Tabla: rutinas

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| nombre | VARCHAR(150) | Nombre de la rutina | NOT NULL |
| tipo | VARCHAR(30) | `calentamiento` / `movilidad` / `vuelta_a_la_calma` | NOT NULL, CHECK (RN22) |
| contraindicaciones | TEXT | Condiciones de salud que la excluyen | — (RN19) |
| descripcion | TEXT | Detalle de la rutina | — |
| entrenador_id | INTEGER | Entrenador que la cargó | FK → entrenadores(id) (RN24) |

## Tabla: rutinas_asignadas

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| alumno_id | INTEGER | Alumno al que se sugirió | NOT NULL, FK → alumnos(id) |
| rutina_id | INTEGER | Rutina sugerida | NOT NULL, FK → rutinas(id) |
| estado | VARCHAR(20) | `pendiente` / `aprobada` / `rechazada` | NOT NULL, CHECK, DEFAULT 'pendiente' (RN21) |
| entrenador_id | INTEGER | Entrenador que aprobó/rechazó | FK → entrenadores(id) (RN24) |
| fecha_validacion | DATE | Fecha de aprobación o rechazo | CHECK `chk_validacion_coherente`: nula si está pendiente, obligatoria (junto con el entrenador) si está aprobada o rechazada |

## Tabla: configuracion

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | INTEGER | Identificador; siempre vale 1 porque la tabla tiene una sola fila | PK, DEFAULT 1, CHECK (id = 1) |
| nombre_gimnasio | VARCHAR(150) | Nombre del gimnasio | NOT NULL |
| dias_aviso_vencimiento | INTEGER | Días para considerar "por vencer" (RN09) | NOT NULL, DEFAULT 7, CHECK (> 0) |
| metodos_pago_habilitados | TEXT[] | Métodos de pago habilitados | NOT NULL |

## Tabla: metas_alumno

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| alumno_id | INTEGER | Alumno al que pertenece la meta | NOT NULL, UNIQUE, FK → alumnos(id) |
| meta_asistencias_semanales | INTEGER | Objetivo semanal de asistencias (RN25) | NOT NULL, DEFAULT 3, CHECK (entre 1 y 7) |
| fecha_actualizacion | DATE | Última modificación de la meta | NOT NULL, DEFAULT hoy |