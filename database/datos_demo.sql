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

-- Alumnos (código de acceso DEMO2026)
INSERT INTO alumnos (nombre, dni, contacto, codigo_acceso_hash, fecha_alta) VALUES
('Camila Rojas', '30111222', '387-5551001', '$2b$12$aQXRgdXiAiqDesjUFDOj.u15NPCxLhASmZc3INuOzQ5xAyxkO/tAe', CURRENT_DATE - 40),
('Marcos Gómez', '31222333', '387-5551002', '$2b$12$aQXRgdXiAiqDesjUFDOj.u15NPCxLhASmZc3INuOzQ5xAyxkO/tAe', CURRENT_DATE - 35),
('Valeria Díaz', '32333444', '387-5551003', '$2b$12$aQXRgdXiAiqDesjUFDOj.u15NPCxLhASmZc3INuOzQ5xAyxkO/tAe', CURRENT_DATE - 28),
('Nicolás Paz', '33444555', '387-5551004', '$2b$12$aQXRgdXiAiqDesjUFDOj.u15NPCxLhASmZc3INuOzQ5xAyxkO/tAe', CURRENT_DATE - 60),
('Sofía Luna', '34555666', '387-5551005', '$2b$12$aQXRgdXiAiqDesjUFDOj.u15NPCxLhASmZc3INuOzQ5xAyxkO/tAe', CURRENT_DATE - 20),
('Diego Herrera', '35666777', '387-5551006', '$2b$12$aQXRgdXiAiqDesjUFDOj.u15NPCxLhASmZc3INuOzQ5xAyxkO/tAe', CURRENT_DATE - 12),
('Julieta Vega', '36777888', '387-5551007', '$2b$12$aQXRgdXiAiqDesjUFDOj.u15NPCxLhASmZc3INuOzQ5xAyxkO/tAe', CURRENT_DATE - 5),
('Tomás Aguirre', '37888999', '387-5551008', '$2b$12$aQXRgdXiAiqDesjUFDOj.u15NPCxLhASmZc3INuOzQ5xAyxkO/tAe', CURRENT_DATE - 2);

-- Inscripciones: tres activas, dos por vencer, dos vencidas y un alumno sin plan
INSERT INTO inscripciones (alumno_id, plan_id, fecha_inicio, fecha_vencimiento, clases_restantes, estado)
SELECT a.id, p.id, CURRENT_DATE - d.inicio, CURRENT_DATE - d.inicio + p.duracion_dias, d.clases, d.estado
FROM (VALUES
    ('30111222', 'Mensual libre', 10, NULL::int, 'activo'),
    ('31222333', 'Trimestral', 15, NULL, 'activo'),
    ('32333444', 'Pack 8 clases', 8, 5, 'activo'),
    ('33444555', 'Mensual libre', 27, NULL, 'por_vencer'),
    ('34555666', 'Mensual libre', 26, NULL, 'por_vencer'),
    ('35666777', 'Mensual libre', 42, NULL, 'vencido'),
    ('36777888', 'Pack 8 clases', 45, 0, 'vencido')
) AS d(dni, plan, inicio, clases, estado)
JOIN alumnos a ON a.dni = d.dni
JOIN planes p ON p.nombre = d.plan;
