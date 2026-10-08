"""Stub de autenticación — change c-03.

TODO(C-02): reemplazar por JWT real (Bearer + roles). Este stub existe solo
para que el change sea autocontenido: ningún test depende de permisos reales
y el punto de integración (dependencia FastAPI) ya queda cableado.
"""

from typing import Any


def get_current_user() -> dict[str, Any]:
    """Devuelve un usuario ficticio con rol de recepcionista."""
    return {"sub": "stub-recepcionista", "roles": ["recepcionista"]}


def require_role(_role: str) -> None:
    """No-op temporal: no valida nada. TODO(C-02): exigir rol del JWT."""
