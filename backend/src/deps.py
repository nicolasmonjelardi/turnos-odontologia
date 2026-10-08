"""Dependencias FastAPI — change c-03.

`get_store` devuelve el store en memoria seedado (sustituible por PG en
cambios futuros). Los tests lo pisan con `dependency_overrides`.
"""

from repos import InMemoryAgendaStore, seed_ficticio

_store_global = seed_ficticio()


def get_store() -> InMemoryAgendaStore:
    return _store_global
