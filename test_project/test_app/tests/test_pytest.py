import pytest

from test_plus.compat import DRF


def test_something(tp):
    response = tp.get('view-200')
    assert response.status_code == 200


@pytest.mark.skipif(DRF is False, reason="DRF is not installed.")
def test_api(tp_api):
    response = tp_api.post('view-json', extra={"format": "json"})
    assert response.status_code == 200
