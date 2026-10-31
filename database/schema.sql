-- Sistema de Gestión para Gimnasios
-- Esquema de base de datos (PostgreSQL)
-- Las claves foráneas usan ON DELETE RESTRICT: no se puede borrar un registro que tenga historial asociado.

CREATE TABLE alumnos (
    id              SERIAL PRIMARY KEY,
    nombre          VARCHAR(150) NOT NULL,
    dni             VARCHAR(20) UNIQUE NOT NULL,
    contacto        VARCHAR(150),
    codigo_acceso_hash  VARCHAR(255) NOT NULL,
    activo          BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_alta      DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE ficha_salud (
    id                  SERIAL PRIMARY KEY,
    alumno_id           INTEGER NOT NULL UNIQUE REFERENCES alumnos(id) ON DELETE RESTRICT,
    problemas_cardiacos BOOLEAN NOT NULL DEFAULT FALSE,
    lesiones            TEXT,
    observaciones       TEXT,
    fecha_registro      DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE planes (
    id                  SERIAL PRIMARY KEY,
    nombre              VARCHAR(100) NOT NULL UNIQUE,
    duracion_dias       INTEGER NOT NULL CHECK (duracion_dias > 0),
    precio              NUMERIC(10,2) NOT NULL CHECK (precio > 0),
    tipo                VARCHAR(20) NOT NULL CHECK (tipo IN ('tiempo', 'clases')),
    cantidad_clases     INTEGER,
    -- Un plan por clases debe indicar su cantidad de clases
    CONSTRAINT chk_plan_clases CHECK (
        (tipo = 'clases' AND cantidad_clases IS NOT NULL AND cantidad_clases > 0)
        OR (tipo = 'tiempo' AND cantidad_clases IS NULL)
    )
);

CREATE TABLE inscripciones (
    id                  SERIAL PRIMARY KEY,
    alumno_id           INTEGER NOT NULL REFERENCES alumnos(id) ON DELETE RESTRICT,
    plan_id             INTEGER NOT NULL REFERENCES planes(id) ON DELETE RESTRICT,
    fecha_inicio        DATE NOT NULL,
    fecha_vencimiento   DATE NOT NULL,
    clases_restantes    INTEGER,
    estado              VARCHAR(20) NOT NULL DEFAULT 'activo'
                         CHECK (estado IN ('activo', 'por_vencer', 'vencido')),
    CONSTRAINT chk_inscripcion_fechas CHECK (fecha_vencimiento >= fecha_inicio),
    -- El saldo de clases nunca puede ser negativo 
    CONSTRAINT chk_inscripcion_saldo CHECK (clases_restantes IS NULL OR clases_restantes >= 0)
);

CREATE TABLE pagos (
    id                  SERIAL PRIMARY KEY,
    inscripcion_id      INTEGER NOT NULL REFERENCES inscripciones(id) ON DELETE RESTRICT,
    fecha_pago          DATE NOT NULL DEFAULT CURRENT_DATE,
    monto               NUMERIC(10,2) NOT NULL CHECK (monto > 0),
    metodo_pago         VARCHAR(20) NOT NULL
                         CHECK (metodo_pago IN ('efectivo', 'transferencia', 'debito', 'credito'))
);

CREATE TABLE asistencias (
    id                  SERIAL PRIMARY KEY,
    alumno_id           INTEGER NOT NULL REFERENCES alumnos(id) ON DELETE RESTRICT,
    inscripcion_id      INTEGER REFERENCES inscripciones(id) ON DELETE RESTRICT,
    fecha               DATE NOT NULL DEFAULT CURRENT_DATE,
    hora                TIME NOT NULL DEFAULT CURRENT_TIME
);

CREATE TABLE entrenadores (
    id              SERIAL PRIMARY KEY,
    nombre          VARCHAR(150) NOT NULL,
    contacto        VARCHAR(150),
    fecha_alta      DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE usuarios (
    id                  SERIAL PRIMARY KEY,
    nombre_usuario      VARCHAR(50) NOT NULL UNIQUE,
    password_hash       VARCHAR(255) NOT NULL,
    rol                 VARCHAR(20) NOT NULL
                         CHECK (rol IN ('administrador', 'entrenador')),
    entrenador_id       INTEGER UNIQUE REFERENCES entrenadores(id) ON DELETE RESTRICT,
    activo              BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_alta          DATE NOT NULL DEFAULT CURRENT_DATE,
    -- Un usuario entrenador debe estar vinculado a un entrenador;
    CONSTRAINT chk_usuario_entrenador CHECK (
        (rol = 'entrenador' AND entrenador_id IS NOT NULL)
        OR (rol <> 'entrenador' AND entrenador_id IS NULL)
    )
);

CREATE TABLE rutinas (
    id                  SERIAL PRIMARY KEY,
    nombre              VARCHAR(150) NOT NULL,
    tipo                VARCHAR(30) NOT NULL
                         CHECK (tipo IN ('calentamiento', 'movilidad', 'vuelta_a_la_calma')),
    contraindicaciones  TEXT,
    descripcion         TEXT,
    entrenador_id       INTEGER REFERENCES entrenadores(id) ON DELETE RESTRICT
);

CREATE TABLE rutinas_asignadas (
    id                  SERIAL PRIMARY KEY,
    alumno_id           INTEGER NOT NULL REFERENCES alumnos(id) ON DELETE RESTRICT,
    rutina_id           INTEGER NOT NULL REFERENCES rutinas(id) ON DELETE RESTRICT,
    estado              VARCHAR(20) NOT NULL DEFAULT 'pendiente'
                         CHECK (estado IN ('pendiente', 'aprobada', 'rechazada')),
    entrenador_id       INTEGER REFERENCES entrenadores(id) ON DELETE RESTRICT,
    fecha_validacion    DATE,
    -- Pendiente: sin entrenador ni fecha. Aprobada o rechazada: con ambos 
    CONSTRAINT chk_validacion_coherente CHECK (
        (estado = 'pendiente' AND entrenador_id IS NULL AND fecha_validacion IS NULL)
        OR (estado IN ('aprobada', 'rechazada') AND entrenador_id IS NOT NULL AND fecha_validacion IS NOT NULL)
    )
);

CREATE TABLE configuracion (
    id                          INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    nombre_gimnasio             VARCHAR(150) NOT NULL,
    dias_aviso_vencimiento      INTEGER NOT NULL DEFAULT 7 CHECK (dias_aviso_vencimiento > 0),
    metodos_pago_habilitados    TEXT[] NOT NULL DEFAULT ARRAY['efectivo','transferencia','debito','credito']
);

CREATE TABLE metas_alumno (
    id                          SERIAL PRIMARY KEY,
    alumno_id                   INTEGER NOT NULL UNIQUE REFERENCES alumnos(id) ON DELETE RESTRICT,
    meta_asistencias_semanales  INTEGER NOT NULL DEFAULT 3 CHECK (meta_asistencias_semanales BETWEEN 1 AND 7),
    fecha_actualizacion         DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Índices básicos para búsquedas frecuentes
CREATE INDEX idx_inscripciones_alumno ON inscripciones(alumno_id);
CREATE INDEX idx_pagos_inscripcion ON pagos(inscripcion_id);
CREATE INDEX idx_asistencias_alumno_fecha ON asistencias(alumno_id, fecha);
CREATE INDEX idx_asistencias_inscripcion ON asistencias(inscripcion_id);