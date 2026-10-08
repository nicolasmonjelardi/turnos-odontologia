"""OPT-IN PG (task 3.2): árbitro EXCLUDE + doble-reserva concurrente.

Se SALTA salvo `TEST_PG=1` + `DATABASE_URL` contra un PG15+ donde el rol
pueda crear la extensión `btree_gist`. Sin PG/Docker (entorno actual de
cátedra) la suite principal sigue verde sin infra externa.
"""

import os

import pytest

pytestmark = pytest.mark.pg_optin

if os.getenv("TEST_PG") != "1" or not os.getenv("DATABASE_URL"):
    pytest.skip("PG opt-in: requiere TEST_PG=1 y DATABASE_URL", allow_module_level=True)


async def test_pg_exclude_rechaza_doble_reserva_solapada():
    from sqlalchemy import text
    from sqlalchemy.exc import IntegrityError
    from sqlalchemy.ext.asyncio import create_async_engine

    engine = create_async_engine(os.environ["DATABASE_URL"])
    try:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS btree_gist"))
            import models

            await conn.run_sync(models.Base.metadata.drop_all)
            await conn.run_sync(models.Base.metadata.create_all)
        from sqlalchemy.ext.asyncio import AsyncSession

        async with AsyncSession(engine) as session:
            session.add(
                models.Turno(profesional_id=1, sillon_id=1, prestacion_id=1, paciente_id=1,
                             inicio="2026-10-15T10:00:00-03:00", fin="2026-10-15T10:30:00-03:00",
                             estado="reservado", token_publico="tok-pg-1")
            )
            await session.commit()
            session.add(
                models.Turno(profesional_id=1, sillon_id=2, prestacion_id=1, paciente_id=2,
                             inicio="2026-10-15T10:15:00-03:00", fin="2026-10-15T10:45:00-03:00",
                             estado="reservado", token_publico="tok-pg-2")
            )
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()
            else:
                raise AssertionError("EXCLUDE debió rechazar la doble reserva")
    finally:
        await engine.dispose()
