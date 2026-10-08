"""Migración 0002_agenda: btree_gist + tablas + 2 EXCLUDE + seed ficticio.

Revision ID: 0002_agenda (replaces: 0001 inicial asumido vacío/greenfield).
"""

from alembic import op

revision = "0002_agenda"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS profesionales (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(120) NOT NULL,
            matricula VARCHAR(40) NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS sillones (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(40) NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS prestaciones (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(120) NOT NULL,
            duracion_min INTEGER NOT NULL,
            CONSTRAINT ck_prestaciones_duracion_pos CHECK (duracion_min > 0)
        );
        CREATE TABLE IF NOT EXISTS pacientes (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(120) NOT NULL,
            dni VARCHAR(20) NOT NULL UNIQUE,
            telefono VARCHAR(40) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS turnos (
            id SERIAL PRIMARY KEY,
            profesional_id INTEGER NOT NULL REFERENCES profesionales(id),
            sillon_id INTEGER NOT NULL REFERENCES sillones(id),
            prestacion_id INTEGER NOT NULL REFERENCES prestaciones(id),
            paciente_id INTEGER NOT NULL REFERENCES pacientes(id),
            inicio TIMESTAMPTZ NOT NULL,
            fin TIMESTAMPTZ NOT NULL,
            estado VARCHAR(20) NOT NULL DEFAULT 'reservado',
            origen VARCHAR(20) NOT NULL DEFAULT 'recepcion',
            token_publico VARCHAR(64) NOT NULL UNIQUE,
            CONSTRAINT ck_turnos_fin_posterior CHECK (fin > inicio)
        );
        CREATE INDEX IF NOT EXISTS ix_turnos_profesional_inicio_fin
            ON turnos (profesional_id, inicio, fin);
        CREATE INDEX IF NOT EXISTS ix_turnos_sillon_inicio_fin
            ON turnos (sillon_id, inicio, fin);
        ALTER TABLE turnos DROP CONSTRAINT IF EXISTS ex_turnos_no_solape_profesional;
        ALTER TABLE turnos ADD CONSTRAINT ex_turnos_no_solape_profesional
            EXCLUDE USING gist (
                profesional_id WITH =,
                tstzrange(inicio, fin, '[)') WITH &&
            ) WHERE (estado <> 'cancelado');
        ALTER TABLE turnos DROP CONSTRAINT IF EXISTS ex_turnos_no_solape_sillon;
        ALTER TABLE turnos ADD CONSTRAINT ex_turnos_no_solape_sillon
            EXCLUDE USING gist (
                sillon_id WITH =,
                tstzrange(inicio, fin, '[)') WITH &&
            ) WHERE (estado <> 'cancelado');
        CREATE TABLE IF NOT EXISTS auditoria (
            id SERIAL PRIMARY KEY,
            turno_id INTEGER NOT NULL REFERENCES turnos(id),
            accion VARCHAR(20) NOT NULL,
            actor VARCHAR(120) NOT NULL,
            creado_en TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    # Seed ficticio (RN11 / Ley 25.326): ver seed_ficticio.sql
    op.execute(
        """
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
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS auditoria")
    op.execute("DROP TABLE IF EXISTS turnos")
    op.execute("DROP TABLE IF EXISTS pacientes")
    op.execute("DROP TABLE IF EXISTS prestaciones")
    op.execute("DROP TABLE IF EXISTS sillones")
    op.execute("DROP TABLE IF EXISTS profesionales")
