import nox

DJANGO_VERSIONS = ["4.2", "5.1", "5.2", "6.0"]
DRF_VERSIONS = ["3.15", "3.16"]
PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13", "3.14", "3.14t"]

INVALID_PYTHON_DJANGO_SESSIONS = [
    ("3.10", "6.0"),
    ("3.11", "6.0"),
    ("3.14", "4.2"),
    ("3.14", "5.1"),
    ("3.14t", "4.2"),
    ("3.14t", "5.1"),
]
INVALID_DRF_DJANGO_SESSIONS = []
INVALID_DRF_PYTHON_SESSIONS = []

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


@nox.session(python=PYTHON_VERSIONS, tags=["drf"], venv_backend="uv")
@nox.parametrize("django", DJANGO_VERSIONS)
@nox.parametrize("drf", DRF_VERSIONS)
def tests_drf(session: nox.Session, django: str, drf: str) -> None:
    if (session.python, django) in INVALID_PYTHON_DJANGO_SESSIONS:
        session.skip()
    if (drf, django) in INVALID_DRF_DJANGO_SESSIONS:
        session.skip()
    if (drf, session.python) in INVALID_DRF_PYTHON_SESSIONS:
        session.skip()
    session.install(".[test]")
    session.install(f"django~={django}")
    session.install(f"djangorestframework~={drf}")
    session.run("pytest", *session.posargs)
