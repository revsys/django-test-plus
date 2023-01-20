import nox

DJANGO_VERSIONS = ["2.2", "3.0", "3.1", "3.2", "4.0", "4.1"]
DRF_VERSIONS = ["3.11", "3.12", "3.13", "3.14"]
PYTHON_VERSIONS = ["3.6", "3.7", "3.8", "3.9", "3.10", "3.11"]

INVALID_PYTHON_DJANGO_SESSIONS = [
    ("3.6", "4.0"),
    ("3.6", "4.1"),
    ("3.6", "4.2"),
    ("3.7", "4.0"),
    ("3.7", "4.1"),
    ("3.7", "4.2"),
    ("3.11", "3.1"),
    ("3.11", "3.2"),
    # ("3.11", "4.0"),
    # ("3.11", "4.1"),
]


@nox.session(python=PYTHON_VERSIONS, tags=["django"])
@nox.parametrize("django", DJANGO_VERSIONS)
def tests(session: nox.Session, django: str) -> None:
    if (session.python, django) in INVALID_PYTHON_DJANGO_SESSIONS:
        session.skip()
    session.install(".[test]")
    session.install(f"django~={django}")
    session.run("pytest", *session.posargs)


@nox.session(python=["3.10"], tags=["drf"])
@nox.parametrize("django", ["3.2"])
@nox.parametrize("drf", DRF_VERSIONS)
def tests_drf(session: nox.Session, django: str, drf: str) -> None:
    session.install(".[test]")
    session.install(f"django~={django}")
    session.install(f"djangorestframework~={drf}")
    session.run("pytest", *session.posargs)
