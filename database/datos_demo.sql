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

-- Pagos: uno por inscripción, con distintos métodos
INSERT INTO pagos (inscripcion_id, fecha_pago, monto, metodo_pago)
SELECT i.id, i.fecha_inicio, p.precio, m.metodo
FROM inscripciones i
JOIN planes p ON p.id = i.plan_id
JOIN alumnos a ON a.id = i.alumno_id
JOIN (VALUES
    ('30111222', 'transferencia'),
    ('31222333', 'credito'),
    ('32333444', 'efectivo'),
    ('33444555', 'efectivo'),
    ('34555666', 'debito'),
    ('35666777', 'efectivo'),
    ('36777888', 'transferencia')
) AS m(dni, metodo) ON m.dni = a.dni;

-- Asistencias de las últimas semanas
INSERT INTO asistencias (alumno_id, inscripcion_id, fecha, hora)
SELECT a.id, i.id, CURRENT_DATE - d.dias, d.hora::time
FROM (VALUES
    ('30111222', 0, '08:15'), ('30111222', 1, '08:20'), ('30111222', 3, '18:40'), ('30111222', 5, '08:10'),
    ('31222333', 0, '19:05'), ('31222333', 2, '19:10'), ('31222333', 4, '19:00'),
    ('32333444', 1, '10:30'), ('32333444', 4, '10:25'), ('32333444', 7, '10:35'),
    ('33444555', 2, '07:50'), ('33444555', 6, '07:45'),
    ('34555666', 0, '17:30'), ('34555666', 3, '17:35')
) AS d(dni, dias, hora)
JOIN alumnos a ON a.dni = d.dni
JOIN inscripciones i ON i.alumno_id = a.id;