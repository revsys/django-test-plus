import nox

DJANGO_VERSIONS = ["3.2", "4.2", "5.0", "5.1"]
DRF_VERSIONS = ["3.11", "3.12", "3.13", "3.14", ]
PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12"]

INVALID_PYTHON_DJANGO_SESSIONS = [
    ("3.9", "5.0"),
    ("3.8", "5.1"),
    ("3.9", "5.1"),
    ("3.11", "3.2"),
    ("3.12", "3.2"),
]

nox.options.default_venv_backend = "uv|venv"
nox.options.reuse_existing_virtualenvs = True


@nox.session(python=PYTHON_VERSIONS, tags=["django"], venv_backend="uv")
@nox.parametrize("django", DJANGO_VERSIONS)
def tests(session: nox.Session, django: str) -> None:
    if (session.python, django) in INVALID_PYTHON_DJANGO_SESSIONS:
        session.skip()
    session.install(".[test]")
    session.install(f"django~={django}")
    session.run("pytest", *session.posargs)


@nox.session(python=["3.10"], tags=["drf"], venv_backend="uv")
@nox.parametrize("django", ["4.2"])
@nox.parametrize("drf", DRF_VERSIONS)
def tests_drf(session: nox.Session, django: str, drf: str) -> None:
    session.install(".[test]")
    session.install(f"django~={django}")
    session.install(f"djangorestframework~={drf}")
    session.run("pytest", *session.posargs)
