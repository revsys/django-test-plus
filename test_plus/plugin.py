import pytest

from .test import BaseTestCase


class TestCase(BaseTestCase):
    """
    pytest plugin version of test_plus.TestCase with helpful additional features
    """
    user_factory = None

    def __init__(self, *args, **kwargs):
        self.last_response = None
        super(TestCase, self).__init__(*args, **kwargs)

    def assertEqual(self, first, second):
        assert first == second, "Elements Not Equal"


@pytest.fixture
def tp(client):
    t = TestCase()
    t.client = client
    return t
