"""Entry point FastAPI — change c-03 (stub-auth, sin SPA).

Router thin: solo cablea routers y expone salud. La lógica vive en
domain/services; la persistencia real (Postgres) es opt-in.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    from routers import health as health_router
    from routers import turnos as turnos_router

    app = FastAPI(title="turnos-odontologia (c-03)")
    app.router.lifespan_context = lifespan
    app.include_router(health_router.router)
    app.include_router(turnos_router.router)
    return app


app = create_app()
