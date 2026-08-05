from importlib import import_module

import pytest

from .compat import get_api_client
from .test import TestCase as BaseTestCase

USER_FACTORY_INI = "test_plus_user_factory"


class TestCase(BaseTestCase):
    """
    pytest plugin version of test_plus.TestCase with helpful additional features
    """

    user_factory = None

    def __init__(self, *args, **kwargs):
        self.last_response = None
        super().__init__(*args, **kwargs)


def pytest_addoption(parser):
    parser.addini(
        USER_FACTORY_INI,
        help=(
            "Dotted path to a factory used by tp.make_user(), for example "
            "myapp.factories.UserFactory. Mirrors the user_factory attribute "
            "on test_plus.TestCase."
        ),
        default=None,
    )


def _load_user_factory(config):
    """Resolve the configured factory, or None when the option is unset."""
    path = config.getini(USER_FACTORY_INI)
    if not path:
        return None

    module_name, _, attr = path.rpartition(".")
    if not module_name:
        raise pytest.UsageError(
            f"{USER_FACTORY_INI} must be a dotted path to a factory, for example "
            f"myapp.factories.UserFactory, got {path!r}"
        )

    try:
        module = import_module(module_name)
    except ImportError as exc:
        raise pytest.UsageError(f"{USER_FACTORY_INI}: cannot import {module_name!r}: {exc}") from exc

    try:
        return getattr(module, attr)
    except AttributeError as exc:
        raise pytest.UsageError(f"{USER_FACTORY_INI}: {module_name!r} has no attribute {attr!r}") from exc


def _make_test_case(config, client):
    factory = _load_user_factory(config)
    # make_user() is a classmethod and reads cls.user_factory, so setting the
    # attribute on the instance would never reach it. Build a subclass instead.
    cls = TestCase if factory is None else type("TestCase", (TestCase,), {"user_factory": factory})
    t = cls()
    t.client = client
    return t


@pytest.fixture
def api_client():
    """Django REST Framework's ``APIClient``, unwrapped.

    Requires djangorestframework to be installed.
    """
    return get_api_client()()


@pytest.fixture
def tp(client, pytestconfig):
    """A ``TestCase`` instance, so every helper is available in pytest tests.

    Anywhere the docs write ``self.get(...)``, a pytest test writes
    ``tp.get(...)``. Ask for pytest-django's ``db`` fixture alongside it in any
    test that touches the database.

    Set the ``test_plus_user_factory`` ini option to a dotted path if
    ``make_user()`` should build users through a factory.
    """
    return _make_test_case(pytestconfig, client)


@pytest.fixture
def tp_api(api_client, pytestconfig):
    """The ``tp`` fixture backed by DRF's ``APIClient``, for testing API views."""
    return _make_test_case(pytestconfig, api_client)
