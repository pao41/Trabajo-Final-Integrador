-- Sistema de Gestión para Gimnasios
-- Esquema de base de datos

CREATE TABLE alumnos (
    id              SERIAL PRIMARY KEY,
    nombre          VARCHAR(150) NOT NULL,
    dni             VARCHAR(20) UNIQUE NOT NULL,
    contacto        VARCHAR(150),
    codigo_acceso   VARCHAR(20) UNIQUE NOT NULL,
    activo          BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_alta      DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE ficha_salud (
    id                  SERIAL PRIMARY KEY,
    alumno_id           INTEGER NOT NULL UNIQUE REFERENCES alumnos(id),
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
    -- El saldo de clases nunca puede ser negativo (RN30)
    CONSTRAINT chk_inscripcion_saldo CHECK (clases_restantes IS NULL OR clases_restantes >= 0)
);

CREATE TABLE pagos (
    id                  SERIAL PRIMARY KEY,
    inscripcion_id      INTEGER NOT NULL REFERENCES inscripciones(id),
    fecha_pago          DATE NOT NULL DEFAULT CURRENT_DATE,
    monto               NUMERIC(10,2) NOT NULL,
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

CREATE TABLE rutinas (
    id                  SERIAL PRIMARY KEY,
    nombre              VARCHAR(150) NOT NULL,
    tipo                VARCHAR(30) NOT NULL
                         CHECK (tipo IN ('calentamiento', 'movilidad', 'vuelta_a_la_calma')),
    contraindicaciones  TEXT,
    descripcion         TEXT,
    entrenador_id       INTEGER REFERENCES entrenadores(id)
);

CREATE TABLE rutinas_asignadas (
    id                  SERIAL PRIMARY KEY,
    alumno_id           INTEGER NOT NULL REFERENCES alumnos(id),
    rutina_id           INTEGER NOT NULL REFERENCES rutinas(id),
    estado              VARCHAR(20) NOT NULL DEFAULT 'pendiente'
                         CHECK (estado IN ('pendiente', 'aprobada', 'rechazada')),
    entrenador_id       INTEGER REFERENCES entrenadores(id),
    fecha_validacion    DATE
);

CREATE TABLE configuracion (
    id                          SERIAL PRIMARY KEY,
    nombre_gimnasio             VARCHAR(150) NOT NULL,
    dias_aviso_vencimiento      INTEGER NOT NULL DEFAULT 7,
    metodos_pago_habilitados    TEXT[] NOT NULL DEFAULT ARRAY['efectivo','transferencia','debito','credito']
);

CREATE TABLE metas_alumno (
    id                          SERIAL PRIMARY KEY,
    alumno_id                   INTEGER NOT NULL UNIQUE REFERENCES alumnos(id),
    meta_asistencias_semanales  INTEGER NOT NULL DEFAULT 3,
    fecha_actualizacion         DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Índices básicos para búsquedas frecuentes
CREATE INDEX idx_inscripciones_alumno ON inscripciones(alumno_id);
CREATE INDEX idx_pagos_inscripcion ON pagos(inscripcion_id);
CREATE INDEX idx_asistencias_alumno_fecha ON asistencias(alumno_id, fecha);