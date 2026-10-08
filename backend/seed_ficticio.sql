-- Seed ficticio (RN11 / Ley 25.326 — NUNCA datos reales).
-- Espejo de alembic/versions/0002_agenda.py para carga manual/psql.
-- Huso America/Argentina/Buenos_Aires (-03). 4 turnos sin choques.

CREATE EXTENSION IF NOT EXISTS btree_gist;

INSERT INTO profesionales (id, nombre, matricula) VALUES
    (1, 'Dra. Ficticia Uno', 'MAT-FICT-001'),
    (2, 'Dr. Ficticio Dos', 'MAT-FICT-002')
ON CONFLICT (id) DO NOTHING;

INSERT INTO sillones (id, nombre) VALUES
    (1, 'Box 1'), (2, 'Box 2')
ON CONFLICT (id) DO NOTHING;

INSERT INTO prestaciones (id, nombre, duracion_min) VALUES
    (1, 'Limpieza', 30), (2, 'Control', 15), (3, 'Obturación', 20),
    (4, 'Endodoncia', 45), (5, 'Ortodoncia', 60)
ON CONFLICT (id) DO NOTHING;

INSERT INTO pacientes (id, nombre, dni, telefono) VALUES
    (1, 'Paciente Ficticio A', 'DNI-FICT-001', '+54-11-0000-0001'),
    (2, 'Paciente Ficticio B', 'DNI-FICT-002', '+54-11-0000-0002'),
    (3, 'Paciente Ficticio C', 'DNI-FICT-003', '+54-11-0000-0003')
ON CONFLICT (id) DO NOTHING;

INSERT INTO turnos
    (id, profesional_id, sillon_id, prestacion_id, paciente_id,
     inicio, fin, estado, origen, token_publico) VALUES
    (1, 1, 1, 1, 1, '2026-10-15 09:00:00-03', '2026-10-15 09:30:00-03',
     'reservado', 'recepcion', 'tok-seed-1'),
    (2, 1, 1, 2, 2, '2026-10-15 10:00:00-03', '2026-10-15 10:15:00-03',
     'reservado', 'recepcion', 'tok-seed-2'),
    (3, 2, 2, 4, 3, '2026-10-15 09:00:00-03', '2026-10-15 09:45:00-03',
     'reservado', 'recepcion', 'tok-seed-3'),
    (4, 2, 2, 1, 1, '2026-10-15 11:00:00-03', '2026-10-15 11:30:00-03',
     'reservado', 'recepcion', 'tok-seed-4')
ON CONFLICT (id) DO NOTHING;
