# Usage

To use django-test-plus, have your tests inherit from test_plus.test.TestCase rather than the normal django.test.TestCase:

```python
from test_plus.test import TestCase

class MyViewTests(TestCase):
    ...
```

This is sufficient to get things rolling, but you are encouraged to create *your own* sub-classes for your projects. This will allow you to add your own project-specific helper methods.

For example, if you have a Django project named 'myproject', you might create the following in `myproject/test.py`:

```python
from test_plus.test import TestCase as PlusTestCase

class TestCase(PlusTestCase):
    pass
```

And then in your tests use:

```python
from myproject.test import TestCase

class MyViewTests(TestCase):
    ...
```

This import, which is similar to the way you would import Django's TestCase, is also valid:

```python
from test_plus import TestCase
```

## pytest Usage {#pytest-usage}

You can get a TestCase like object as a pytest fixture now by asking for <span class="title-ref">tp</span>. All of the methods below would then work in pytest functions. For example:

```python
def test_url_reverse(tp):
    expected_url = '/api/'
    reversed_url = tp.reverse('api')
    assert expected_url == reversed_url
```

Everything documented in `methods`, `auth_helpers`, `low_query_counts` and `cbvtestcase` is available on `tp`. Anywhere those pages write `self.<method>()`, a pytest test writes `tp.<method>()`. The same test written both ways:

```python
# unittest style
from test_plus.test import TestCase

class MyViewTests(TestCase):

    def test_the_view(self):
        self.get('my-url-name')
        self.response_200()
        self.assertInContext('some-key')

    def test_auth(self):
        user = self.make_user('u1')
        self.assertLoginRequired('my-protected-view')
        with self.login(user):
            self.get_check_200('my-protected-view')

# pytest style
def test_the_view(tp):
    tp.get('my-url-name')
    tp.response_200()
    tp.assertInContext('some-key')

def test_auth(tp, db):
    user = tp.make_user('u1')
    tp.assertLoginRequired('my-protected-view')
    with tp.login(user):
        tp.get_check_200('my-protected-view')
```

Note that `tp` does not manage database access for you the way `django.test.TestCase` does. Ask for pytest-django's `db` fixture (or apply `@pytest.mark.django_db`) in any test that touches the database. That includes `make_user()` and the `login()` context, and also the query counting helpers `assertNumQueriesLessThan()` and `assertGoodView()`, which open a database connection in order to count.

The pytest plugin is auto-registered via `pytest11`, so no extra configuration is required beyond installing the package and pytest-django. In addition to `tp` and `tp_api`, the plugin also provides a raw `api_client` fixture:

```python
def test_api_client(api_client):
    response = api_client.get("/api/")
    assert response.status_code == 200
```

The `tp_api` fixture will provide a `TestCase` that uses django-rest-framework's \`APIClient()\`:

```python
def test_url_reverse(tp_api):
    response = tp_api.client.post("myapi", format="json")
    assert response.status_code == 200
```

## Testing DRF views

To take advantage of the convenience of DRF's test client, you can create a subclass of `TestCase` and set the `client_class` property:

```python
from test_plus import TestCase
from rest_framework.test import APIClient

class APITestCase(TestCase):
    client_class = APIClient
```

For convenience, `test_plus` ships with `APITestCase`, which does just that:

```python
from test_plus import APITestCase

class MyAPITestCase(APITestCase):

    def test_post(self):
        data = {'testing': {'prop': 'value'}}
        self.post('view-json', data=data, extra={'format': 'json'})
        self.response_200()
```

Note that using `APITestCase` requires Django \>= 1.8 and having installed `django-rest-framework`.
