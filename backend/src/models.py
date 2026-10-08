"""Modelos SQLAlchemy async — change c-03.

`timestamptz` en inicio/fin; `duracion_min > 0` CHECK; índices
(profesional|sillon, inicio, fin); 2 EXCLUDE USING gist como árbitro
de concurrencia (requiere extensión `btree_gist`).

El upgrade real contra PG15 es opt-in (TEST_PG=1); la estructura se
verifica offline compilando DDL en dialecto postgresql.
"""

from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Table,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Profesional(Base):
    __tablename__ = "profesionales"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    matricula: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)


class Sillon(Base):
    __tablename__ = "sillones"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)  # "Box 1"


class Prestacion(Base):
    __tablename__ = "prestaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    duracion_min: Mapped[int] = mapped_column(nullable=False)

    __table_args__ = (CheckConstraint("duracion_min > 0", name="ck_prestaciones_duracion_pos"),)


class Paciente(Base):
    __tablename__ = "pacientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    dni: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    telefono: Mapped[str] = mapped_column(String(40), nullable=False)


class Turno(Base):
    __tablename__ = "turnos"

    id: Mapped[int] = mapped_column(primary_key=True)
    profesional_id: Mapped[int] = mapped_column(ForeignKey("profesionales.id"), nullable=False)
    sillon_id: Mapped[int] = mapped_column(ForeignKey("sillones.id"), nullable=False)
    prestacion_id: Mapped[int] = mapped_column(ForeignKey("prestaciones.id"), nullable=False)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"), nullable=False)
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fin: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False, default="reservado")
    origen: Mapped[str] = mapped_column(String(20), nullable=False, default="recepcion")
    token_publico: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    __table_args__ = (
        Index("ix_turnos_profesional_inicio_fin", "profesional_id", "inicio", "fin"),
        Index("ix_turnos_sillon_inicio_fin", "sillon_id", "inicio", "fin"),
        CheckConstraint("fin > inicio", name="ck_turnos_fin_posterior"),
    )


class Auditoria(Base):
    __tablename__ = "auditoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    turno_id: Mapped[int] = mapped_column(ForeignKey("turnos.id"), nullable=False)
    accion: Mapped[str] = mapped_column(String(20), nullable=False)  # "crear"
    actor: Mapped[str] = mapped_column(String(120), nullable=False)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


# Árbitro de concurrencia: dos EXCLUDE parciales (filas no canceladas).
# Se agregan post-clase para referenciar columnas como objetos.
_turnos_table = Turno.__table__
assert isinstance(_turnos_table, Table)
_turnos_table.append_constraint(
    ExcludeConstraint(
        (Turno.profesional_id, "="),
        (func.tstzrange(Turno.inicio, Turno.fin, "[)"), "&&"),
        where=text("estado <> 'cancelado'"),
        name="ex_turnos_no_solape_profesional",
        using="gist",
    )
)
_turnos_table.append_constraint(
    ExcludeConstraint(
        (Turno.sillon_id, "="),
        (func.tstzrange(Turno.inicio, Turno.fin, "[)"), "&&"),
        where=text("estado <> 'cancelado'"),
        name="ex_turnos_no_solape_sillon",
        using="gist",
    )
)
