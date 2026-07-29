from django.test import TestCase as DjangoTestCase

# Re-exported for convenience so callers can import them from test_plus.compat.
from django.urls import NoReverseMatch, reverse  # noqa: F401

try:
    import rest_framework  # noqa

    DRF = True
except ImportError:
    DRF = False


def get_api_client():
    try:
        from rest_framework.test import APIClient
    except ImportError:
        from django.core.exceptions import ImproperlyConfigured

        def APIClient(*args, **kwargs):
            raise ImproperlyConfigured("django-rest-framework must be installed in order to use APITestCase.")

    return APIClient


assertURLEqual = DjangoTestCase.assertURLEqual


try:
    from django.contrib.messages.test import MessagesTestMixin

    assertMessages = MessagesTestMixin.assertMessages
except ImportError:

    def assertMessages(t, response, expected_messages, ordered=True):
        raise NotImplementedError(
            "Your version of Django does not support `assertMessages`. "
            "This method is only available in Django 5.0 and later."
        )
