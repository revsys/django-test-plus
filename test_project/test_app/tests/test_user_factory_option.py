"""Tests for the test_plus_user_factory pytest option.

The option is read from the ini file, so the end to end check runs pytest in a
subprocess with -o rather than trying to mutate config in process.
"""

import subprocess
import sys
from pathlib import Path

import pytest

from test_plus.plugin import USER_FACTORY_INI, _load_user_factory

REPO_ROOT = Path(__file__).resolve().parents[3]


class FakeConfig:
    def __init__(self, value):
        self._value = value

    def getini(self, name):
        assert name == USER_FACTORY_INI
        return self._value


def test_unset_returns_none():
    assert _load_user_factory(FakeConfig(None)) is None


def test_empty_string_returns_none():
    assert _load_user_factory(FakeConfig("")) is None


def test_loads_a_dotted_path():
    from test_app.factories import UserFactory

    assert _load_user_factory(FakeConfig("test_app.factories.UserFactory")) is UserFactory


def test_rejects_a_path_without_a_module():
    with pytest.raises(pytest.UsageError, match="dotted path"):
        _load_user_factory(FakeConfig("UserFactory"))


def test_reports_an_unimportable_module():
    with pytest.raises(pytest.UsageError, match="cannot import"):
        _load_user_factory(FakeConfig("test_app.nope.UserFactory"))


def test_reports_a_missing_attribute():
    with pytest.raises(pytest.UsageError, match="has no attribute"):
        _load_user_factory(FakeConfig("test_app.factories.NotAFactory"))


def test_tp_uses_the_configured_factory(tmp_path):
    """End to end: with the ini set, tp.make_user() goes through the factory."""
    test_file = tmp_path / "test_uses_factory.py"
    test_file.write_text(
        "def test_make_user_uses_the_factory(tp, db):\n"
        "    user = tp.make_user('passed-through')\n"
        "    assert tp.user_factory is not None\n"
        "    # make_user passes the username to the factory, so it wins, but the\n"
        "    # email comes from the factory's own sequence. Without the option\n"
        "    # that would be passed-through@example.com instead.\n"
        "    assert user.username == 'passed-through'\n"
        "    assert user.email.startswith('factoryuser')\n"
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(test_file),
            "-o",
            f"{USER_FACTORY_INI}=test_app.factories.UserFactory",
            "-o",
            "DJANGO_SETTINGS_MODULE=test_project.settings",
            "-o",
            "pythonpath=test_project",
            "-p",
            "no:cacheprovider",
            "-q",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
