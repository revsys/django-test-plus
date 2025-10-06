from django.test import TestCase as DjangoTestCase

try:
    from django.urls import reverse, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, NoReverseMatch  # noqa

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
            raise ImproperlyConfigured('django-rest-framework must be installed in order to use APITestCase.')
    return APIClient


if hasattr(DjangoTestCase, 'assertURLEqual'):
    assertURLEqual = DjangoTestCase.assertURLEqual
else:
    def assertURLEqual(t, url1, url2, msg_prefix=''):
        raise NotImplementedError("Your version of Django does not support `assertURLEqual`")


try:
    from django.contrib.messages.test import MessagesTestMixin
    assertMessages = MessagesTestMixin.assertMessages
except ImportError:
    def assertMessages(t, response, expected_messages, ordered=True):
        raise NotImplementedError(
            "Your version of Django does not support `assertMessages`. "
            "This method is only available in Django 5.0 and later."
        )
