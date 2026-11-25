-- Datos de demostración del Sistema de Gestión para Gimnasios.
-- Se ejecuta una sola vez, sobre la base creada con schema.sql y con el administrador ya creado.
-- Las fechas se calculan a partir del día de ejecución, por lo que los estados de los planes son vigentes.
--
-- Credenciales de demostración:
--   Entrenador: usuario entrenadora_demo, contraseña Demo-12345
--   Alumnos (panel del alumno): DNI de la tabla alumnos, código de acceso DEMO2026

-- Configuración del gimnasio
INSERT INTO configuracion (id, nombre_gimnasio, dias_aviso_vencimiento)
VALUES (1, 'Gimnasio Demo', 7)
ON CONFLICT (id) DO NOTHING;

-- Entrenadora y su usuario de acceso
INSERT INTO entrenadores (nombre, contacto)
VALUES ('Lucía Fernández', '387-4001234');

INSERT INTO usuarios (nombre_usuario, password_hash, rol, entrenador_id)
SELECT 'entrenadora_demo', '$2b$12$lVqok352EygfbSqx0nrU1uVo1D2DFMhsIXGneGGfxHpRBH9wKej0W', 'entrenador', id
FROM entrenadores WHERE nombre = 'Lucía Fernández';

-- Planes
INSERT INTO planes (nombre, duracion_dias, precio, tipo, cantidad_clases) VALUES
('Mensual libre', 30, 25000, 'tiempo', NULL),
('Trimestral', 90, 65000, 'tiempo', NULL),
('Pack 8 clases', 30, 18000, 'clases', 8);