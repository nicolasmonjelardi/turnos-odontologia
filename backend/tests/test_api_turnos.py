"""RED task 4.1: POST /api/turnos thin (201/409/422 contractuales).

httpx ASGITransport + dependency_overrides[get_store] con store fresco.
Sin PG, sin JWT real.
"""

from httpx import ASGITransport, AsyncClient


def _payload(**over):
    base = {
        "profesional_id": 1,
        "sillon_id": 1,
        "prestacion_id": 1,  # 30 min
        "paciente_id": 1,
        "inicio": "2026-10-15T12:00:00-03:00",
    }
    base.update(over)
    return base


def _client(store):
    from deps import get_store
    from main import create_app

    app = create_app()
    app.dependency_overrides[get_store] = lambda: store
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


async def test_post_feliz_201_con_fin_y_auditoria():
    from repos import seed_ficticio

    store = seed_ficticio()
    async with _client(store) as client:
        resp = await client.post("/api/turnos", json=_payload())
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["estado"] == "reservado"
    assert body["fin"] == "2026-10-15T12:30:00-03:00"
    assert body["token_publico"]
    assert any(a.accion == "crear" and a.turno_id == body["id"] for a in store.auditoria)


async def test_post_solape_profesional_409_identificado_sin_persistir():
    from repos import seed_ficticio

    store = seed_ficticio()  # t1: prof1 [09:00,09:30)
    n_antes, a_antes = len(store.turnos), len(store.auditoria)
    async with _client(store) as client:
        resp = await client.post(
            "/api/turnos",
            json=_payload(profesional_id=1, sillon_id=2, inicio="2026-10-15T09:15:00-03:00"),
        )
    assert resp.status_code == 409, resp.text
    assert resp.json()["codigo"] == "PROFESIONAL_OCUPADO"
    assert resp.json()["conflicto"]["turno_id"] == 1
    assert len(store.turnos) == n_antes and len(store.auditoria) == a_antes


async def test_post_solape_sillon_409_aunque_profesional_libre():
    from repos import seed_ficticio

    store = seed_ficticio()  # t3: sillon2 [09:00,09:45); prof1 libre [09:30,10:00)
    async with _client(store) as client:
        resp = await client.post(
            "/api/turnos",
            json=_payload(profesional_id=1, sillon_id=2, inicio="2026-10-15T09:30:00-03:00"),
        )
    assert resp.status_code == 409, resp.text
    assert resp.json()["codigo"] == "SILLON_OCUPADO"


async def test_post_borde_fin_igual_inicio_201():
    from repos import seed_ficticio

    store = seed_ficticio()  # t2: prof1/sillon1 termina 10:15
    async with _client(store) as client:
        resp = await client.post(
            "/api/turnos",
            json=_payload(prestacion_id=2, inicio="2026-10-15T10:15:00-03:00"),  # 15 min
        )
    assert resp.status_code == 201, resp.text


async def test_post_duracion_variable_cambia_el_resultado():
    from repos import seed_ficticio

    store = seed_ficticio()  # t4: prof2/sillon2 [11:00,11:30)
    larga = _payload(profesional_id=2, sillon_id=2, prestacion_id=3,  # 20 min → fin 11:05
                     inicio="2026-10-15T10:45:00-03:00")
    corta = _payload(profesional_id=2, sillon_id=2, prestacion_id=2,  # 15 min → fin 11:00
                     inicio="2026-10-15T10:45:00-03:00")
    async with _client(store) as client:
        r_larga = await client.post("/api/turnos", json=larga)
        assert r_larga.status_code == 409, r_larga.text
        r_corta = await client.post("/api/turnos", json=corta)
        assert r_corta.status_code == 201, r_corta.text


async def test_post_fecha_naive_422_sin_persistir():
    from repos import seed_ficticio

    store = seed_ficticio()
    n_antes = len(store.turnos)
    async with _client(store) as client:
        resp = await client.post("/api/turnos", json=_payload(inicio="2026-10-15T12:00:00"))
    assert resp.status_code == 422, resp.text
    assert len(store.turnos) == n_antes and store.auditoria == []
