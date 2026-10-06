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