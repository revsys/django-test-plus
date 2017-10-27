try:
    from django.urls import reverse, NoReverseMatch
except ImportError:
    from django.core.urlresolvers import reverse, NoReverseMatch  # noqa

try:
    from rest_framework.test import APIClient
    DRF = True
except ImportError:
    from django.core.exceptions import ImproperlyConfigured

    def APIClient(*args, **kwargs):
        raise ImproperlyConfigured('django-rest-framework must be installed in order to use APITestCase.')
    DRF = False
