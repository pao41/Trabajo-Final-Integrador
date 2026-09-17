-- Sistema de Gestión para Gimnasios
-- Esquema de base de datos (PostgreSQL)

CREATE TABLE alumnos (
    id              SERIAL PRIMARY KEY,
    nombre          VARCHAR(150) NOT NULL,
    dni             VARCHAR(20) UNIQUE NOT NULL,
    contacto        VARCHAR(150),
    codigo_acceso   VARCHAR(20) UNIQUE NOT NULL,
    fecha_alta      DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE ficha_salud (
    id                  SERIAL PRIMARY KEY,
    alumno_id           INTEGER NOT NULL REFERENCES alumnos(id),
    problemas_cardiacos BOOLEAN NOT NULL DEFAULT FALSE,
    lesiones            TEXT,
    observaciones       TEXT,
    fecha_registro      DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE planes (
    id              SERIAL PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    duracion_dias   INTEGER NOT NULL,
    precio          NUMERIC(10,2) NOT NULL,
    tipo            VARCHAR(20) NOT NULL CHECK (tipo IN ('tiempo', 'clases'))
);

CREATE TABLE inscripciones (
    id                  SERIAL PRIMARY KEY,
    alumno_id           INTEGER NOT NULL REFERENCES alumnos(id),
    plan_id             INTEGER NOT NULL REFERENCES planes(id),
    fecha_inicio        DATE NOT NULL,
    fecha_vencimiento   DATE NOT NULL,
    estado              VARCHAR(20) NOT NULL DEFAULT 'activo'
                         CHECK (estado IN ('activo', 'por_vencer', 'vencido'))
);

