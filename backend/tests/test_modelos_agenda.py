"""Modelos async con timestamptz, CHECK, índices y EXCLUDE (task 3.1).

Verificación offline (sin PG vivo): compila DDL en dialecto postgresql y
contiene EXCLUDE + gist. El upgrade real contra PG15 es opt-in
(test_pg_exclude_optin.py, TEST_PG=1).
"""

from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

import models


def test_modelos_exponen_tablas_agenda():
    nombres = set(models.Base.metadata.tables)
    assert {"profesionales", "sillones", "prestaciones", "pacientes", "turnos", "auditoria"} <= nombres


def test_turno_ddl_contiene_exclude_btree_gist():
    create = str(CreateTable(models.Turno.__table__).compile(dialect=postgresql.dialect()))
    assert "EXCLUDE" in create
    assert "gist" in create
    assert "tstzrange" in create


def test_prestacion_exige_duracion_positiva_en_ddl():
    create = str(CreateTable(models.Prestacion.__table__).compile(dialect=postgresql.dialect()))
    assert "duracion_min" in create
    assert "CHECK" in create
