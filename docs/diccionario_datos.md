# Diccionario de Datos — Sistema de Gestión para Gimnasios

## Tabla: alumnos

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único del alumno | PK |
| nombre | VARCHAR(150) | Nombre completo | NOT NULL |
| dni | VARCHAR(20) | Documento de identidad | NOT NULL, UNIQUE (RN13) |
| contacto | VARCHAR(150) | Teléfono o email de contacto | — |
| codigo_acceso | VARCHAR(20) | Código para el Panel del Alumno | NOT NULL, UNIQUE |
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
| duracion_dias | INTEGER | Duración del plan en días | NOT NULL |
| precio | NUMERIC(10,2) | Precio del plan | NOT NULL |
| tipo | VARCHAR(20) | `tiempo` o `clases` | NOT NULL, CHECK |

## Tabla: inscripciones

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| alumno_id | INTEGER | Alumno inscripto | NOT NULL, FK → alumnos(id) |
| plan_id | INTEGER | Plan contratado | NOT NULL, FK → planes(id) |
| fecha_inicio | DATE | Inicio del período contratado | NOT NULL |
| fecha_vencimiento | DATE | Vencimiento calculado (RN02) | NOT NULL |
| estado | VARCHAR(20) | `activo` / `por_vencer` / `vencido` | NOT NULL, CHECK, DEFAULT 'activo' (RN01) |

## Tabla: pagos

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| inscripcion_id | INTEGER | Inscripción asociada | NOT NULL, FK → inscripciones(id) |
| fecha_pago | DATE | Fecha en que se registró el pago | NOT NULL, DEFAULT hoy |
| monto | NUMERIC(10,2) | Monto abonado | NOT NULL (RN05: siempre valor completo del período) |
| metodo_pago | VARCHAR(20) | `efectivo` / `transferencia` / `debito` / `credito` | NOT NULL, CHECK (RN27) |

## Tabla: asistencias

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| alumno_id | INTEGER | Alumno que registró ingreso | NOT NULL, FK → alumnos(id) |
| fecha | DATE | Fecha del check-in | NOT NULL, DEFAULT hoy |
| hora | TIME | Hora del check-in | NOT NULL, DEFAULT ahora |

## Tabla: entrenadores

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| nombre | VARCHAR(150) | Nombre del entrenador | NOT NULL |
| contacto | VARCHAR(150) | Teléfono o email | — |
| fecha_alta | DATE | Fecha de alta en el sistema | NOT NULL, DEFAULT hoy |

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
| fecha_validacion | DATE | Fecha de aprobación o rechazo | — |

## Tabla: configuracion

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| nombre_gimnasio | VARCHAR(150) | Nombre del gimnasio | NOT NULL |
| dias_aviso_vencimiento | INTEGER | Días para considerar "por vencer" (RN09) | NOT NULL, DEFAULT 7 |
| metodos_pago_habilitados | TEXT[] | Métodos de pago habilitados | NOT NULL |

## Tabla: metas_alumno

| Columna | Tipo | Descripción | Restricciones |
|---|---|---|---|
| id | SERIAL | Identificador único | PK |
| alumno_id | INTEGER | Alumno al que pertenece la meta | NOT NULL, UNIQUE, FK → alumnos(id) |
| meta_asistencias_semanales | INTEGER | Objetivo semanal de asistencias (RN25) | NOT NULL, DEFAULT 3 |
| fecha_actualizacion | DATE | Última modificación de la meta | NOT NULL, DEFAULT hoy |