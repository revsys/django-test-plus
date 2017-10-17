from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch  # noqa

try:
    from rest_framework.test import APIClient
    DRF = True
except ImportError:
    def APIClient(*args, **kwargs):
        raise ImproperlyConfigured('django-rest-framework must be installed in order to use APITestCase.')
    DRF = False
