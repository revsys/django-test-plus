import pytest

from test_plus.compat import DRF


def test_something(tp):
    response = tp.get("view-200")
    assert response.status_code == 200


@pytest.mark.skipif(DRF is False, reason="DRF is not installed.")
def test_api(tp_api):
    response = tp_api.post("view-json", extra={"format": "json"})
    assert response.status_code == 200


def test_assert_login_required(tp):
    tp.assertLoginRequired("view-needs-login")


def test_assert_in_context(tp):
    response = tp.get("view-context-with")
    assert "testvalue" in response.context
    tp.assertInContext("testvalue")


def test_user_factory_defaults_to_none(tp):
    # Without the ini option set, tp behaves exactly as before.
    assert tp.user_factory is None


def test_make_user_without_a_factory(tp, db):
    user = tp.make_user("plain")
    assert user.username == "plain"
