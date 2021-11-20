import pytest

from .compat import get_api_client
from .test import TestCase as BaseTestCase


class TestCase(BaseTestCase):
    """
    pytest plugin version of test_plus.TestCase with helpful additional features
    """
    user_factory = None

    def __init__(self, *args, **kwargs):
        self.last_response = None
        super(TestCase, self).__init__(*args, **kwargs)


@pytest.fixture
def api_client():
    return get_api_client()()


@pytest.fixture
def tp(client):
    t = TestCase()
    t.client = client
    return t


@pytest.fixture
def tp_api(api_client):
    t = TestCase()
    t.client = api_client
    return t
