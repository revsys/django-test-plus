@_default:
    just --list

# Install development dependencies
@bootstrap:
    python -m pip install --upgrade pip uv
    python -m uv pip install --upgrade nox

# Run bumpver with optional arguments
@bump *ARGS="--help":
    uv tool run bumpver {{ ARGS }}

# Bump patch version (dry run by default, use ARGS="" to apply)
@bump-patch *ARGS="--dry":
    uv tool run bumpver update --patch {{ ARGS }}
    uv lock

# Bump minor version (dry run by default, use ARGS="" to apply)
@bump-minor *ARGS="--dry":
    uv tool run bumpver update --minor {{ ARGS }}
    uv lock

# Run test coverage report
@coverage *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "coverage"

# Build documentation
@docs *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "docs"

# Format justfile
@fmt:
    just --fmt --unstable

# Run linting checks
@lint *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "lint"

# Compile requirements lock file
@lock:
    python -m piptools compile --resolver=backtracking

# Run all nox sessions
@nox *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }}

# Build and publish a release to PyPI
@release:
    rm -rf build dist
    uv build
    git push --tags
    uv publish

# Run all tests
@test *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }}

# Run tests with Django REST Framework
@test-drf *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "tests_drf"

# Run tests in current environment
@test-env *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "tests_env"

# Run tests with latest Python and Django versions
@test-latest *ARGS="--no-install --reuse-existing-virtualenvs":
    python -m nox {{ ARGS }} --session "tests-3.12(django='5.1')"
