Usage
-----

To use django-test-plus, have your tests inherit
from test\_plus.test.TestCase rather than the normal
django.test.TestCase::

    from test_plus.test import TestCase

    class MyViewTests(TestCase):
        ...

This is sufficient to get things rolling, but you are encouraged to
create *your own* sub-classes for your projects. This will allow you
to add your own project-specific helper methods.

For example, if you have a Django project named 'myproject', you might
create the following in ``myproject/test.py``::

    from test_plus.test import TestCase as PlusTestCase

    class TestCase(PlusTestCase):
        pass

And then in your tests use::

    from myproject.test import TestCase

    class MyViewTests(TestCase):
        ...

This import, which is similar to the way you would import Django's TestCase, 
is also valid::

    from test_plus import TestCase

pytest Usage
~~~~~~~~~~~~

You can get a TestCase like object as a pytest fixture now by asking for `tp`. All of the methods below would then work in pytest functions. For
example::

    def test_url_reverse(tp):
        expected_url = '/api/'
        reversed_url = tp.reverse('api')
        assert expected_url == reversed_url

The ``tp_api`` fixture will provide a ``TestCase`` that uses django-rest-framework's `APIClient()`::

    def test_url_reverse(tp_api):
        response = tp_api.client.post("myapi", format="json")
        assert response.status_code == 200


Testing DRF views
~~~~~~~~~~~~~~~~~

To take advantage of the convenience of DRF's test client, you can create a subclass of ``TestCase`` and set the ``client_class`` property::

    from test_plus import TestCase
    from rest_framework.test import APIClient


    class APITestCase(TestCase):
        client_class = APIClient

For convenience, ``test_plus`` ships with ``APITestCase``, which does just that::

    from test_plus import APITestCase


    class MyAPITestCase(APITestCase):

        def test_post(self):
            data = {'testing': {'prop': 'value'}}
            self.post('view-json', data=data, extra={'format': 'json'})
            self.response_200()

Note that using ``APITestCase`` requires Django >= 1.8 and having installed ``django-rest-framework``.
