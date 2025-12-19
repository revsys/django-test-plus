@_default:
    just --list

@bootstrap:
    python -m pip install --upgrade pip uv
    python -m uv pip install --upgrade nox

# Bump version (use: just bump patch, just bump minor, just bump major)
@bump *ARGS="--help":
    uv tool run bumpver {{ ARGS }}

@coverage *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "coverage"

@docs *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "docs"

@fmt:
    just --fmt --unstable

@lint *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "lint"

@lock:
    python -m piptools compile --resolver=backtracking

@nox *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }}

@test *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }}

@test-drf *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "tests_drf"

@test-latest *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "tests-3.12(django='5.1')"

# @test-alphas *ARGS="--no-install --reuse-existing-virtualenvs":
#     python -m nox {{ ARGS }} --session "tests-3.12(django='5.1a1')"

@test-env *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "tests_env"

# Build and publish a release to PyPI
@release:
    rm -rf build dist
    python setup.py sdist bdist_wheel
    git push --tags
    twine upload dist/*
