"""RED task 1.2: stub-auth importa sin JWT real y es no-op documentado."""


def test_auth_stub_sin_jwt_real():
    from auth_stub import get_current_user, require_role

    user = get_current_user()
    assert user["sub"] == "stub-recepcionista"
    assert "recepcionista" in user["roles"]
    # require_role es no-op: no lanza aunque el rol no exista aún (TODO C-02)
    require_role("cualquier-rol")


def test_auth_stub_no_depende_de_libreria_jwt():
    import subprocess

    code = (
        "import sys; sys.path.insert(0, 'src');"
        "assert 'jwt' not in sys.modules;"
        "import auth_stub;"
        "print(auth_stub.get_current_user()['sub'])"
    )
    proc = subprocess.run(
        ["python", "-c", code], capture_output=True, text=True, cwd=".", check=False
    )
    assert proc.returncode == 0, proc.stderr
    assert "stub-recepcionista" in proc.stdout
