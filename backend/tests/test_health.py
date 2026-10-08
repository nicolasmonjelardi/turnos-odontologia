"""RED task 1.1: la app expone GET /api/health. Sin PG, sin auth."""

from httpx import ASGITransport, AsyncClient


async def test_health_responde_ok():
    from main import create_app

    transport = ASGITransport(app=create_app())
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_factory_devuelve_instancias_independientes():
    from fastapi import FastAPI

    from main import create_app

    app1, app2 = create_app(), create_app()
    assert isinstance(app1, FastAPI)
    assert app1 is not app2
