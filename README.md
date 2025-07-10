# django-test-plus

Useful additions to Django's default TestCase from [REVSYS](https://www.revsys.com/)

[![pypi](https://img.shields.io/pypi/v/django-test-plus.svg)](https://pypi.org/project/django-test-plus/)
[![build matrix demo](https://github.com/revsys/django-test-plus/actions/workflows/actions.yml/badge.svg)](https://github.com/revsys/django-test-plus/actions/workflows/actions.yml)

## Rationale

Let's face it, writing tests isn't always fun. Part of the reason for
that is all of the boilerplate you end up writing. django-test-plus is
an attempt to cut down on some of that when writing Django tests. We
guarantee it will increase the time before you get carpal tunnel by at
least 3 weeks!

If you would like to get started testing your Django apps or improve how your
team is testing we offer [TestStart](https://www.revsys.com/teststart/)
to help your team dramatically improve your productivity.

## Support

- Python 3.9, 3.10, 3.11, 3.12, and 3.13.

- Django 4.2 LTS, 5.1, and 5.2 LTS.

## Documentation

Full documentation is available at http://django-test-plus.readthedocs.org

## Installation

```shell
$ pip install django-test-plus
```

## Usage

To use django-test-plus, have your tests inherit from test_plus.test.TestCase rather than the normal django.test.TestCase::

```python
from test_plus.test import TestCase

class MyViewTests(TestCase):
    ...
```

This is sufficient to get things rolling, but you are encouraged to
create *your own* sub-classes for your projects. This will allow you
to add your own project-specific helper methods.

For example, if you have a django project named 'myproject', you might
create the following in `myproject/test.py`:

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

This import, which is similar to the way you would import Django's TestCase,
is also valid:

```python
from test_plus import TestCase
```

## pytest Usage

Django-test-plus provides comprehensive pytest integration through fixtures and a pytest plugin. The plugin is automatically registered when you install django-test-plus.

### Basic Fixtures

#### `tp` fixture
You can get a TestCase-like object as a pytest fixture by asking for `tp`. All of the methods below will work in pytest functions:

```python
def test_url_reverse(tp):
    expected_url = '/api/'
    reversed_url = tp.reverse('api')
    assert expected_url == reversed_url

def test_user_creation(tp):
    user = tp.make_user('testuser')
    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'

def test_view_with_context(tp):
    tp.get('my-view')
    tp.assertInContext('some-key')
    tp.assertContext('some-key', 'expected-value')
```

#### `tp_api` fixture
The `tp_api` fixture provides a TestCase that uses django-rest-framework's `APIClient()`:

```python
def test_api_endpoint(tp_api):
    response = tp_api.client.post("myapi", format="json")
    assert response.status_code == 200
    
def test_api_with_auth(tp_api):
    user = tp_api.make_user('apiuser')
    with tp_api.login(user):
        response = tp_api.get('protected-api')
        tp_api.assert_http_200_ok(response)
```

### Advanced pytest Integration

#### All TestCase methods available
Both `tp` and `tp_api` fixtures provide access to all django-test-plus TestCase methods:

```python
def test_comprehensive_view(tp):
    # URL helpers
    response = tp.get('my-view')
    
    # Response testing
    tp.assertResponseContains('Welcome')
    tp.assertResponseHeaders({'Content-Type': 'text/html'})
    
    # Status code assertions
    tp.assert_http_200_ok()
    
    # Context testing
    tp.assertInContext('user')
    tp.assertContext('title', 'My Page')
    
    # Query count testing
    with tp.assertNumQueriesLessThan(5):
        tp.get('efficient-view')
```

#### Mixed with pytest features
You can combine django-test-plus fixtures with other pytest features:

```python
import pytest

@pytest.mark.django_db
def test_database_operations(tp):
    user = tp.make_user('dbuser')
    assert user.pk is not None
    
@pytest.mark.parametrize('username', ['user1', 'user2', 'admin'])
def test_multiple_users(tp, username):
    user = tp.make_user(username)
    assert user.username == username
    assert user.email == f'{username}@example.com'

def test_form_errors(tp):
    response = tp.post('form-view', data={})
    tp.print_form_errors(response)  # Debug helper
```

### Plugin Registration
The pytest plugin is automatically registered via entry points in `setup.cfg`. No additional configuration is needed - just install django-test-plus and the fixtures will be available.

## Methods

### `reverse(url_name, *args, **kwargs)`

When testing views you often find yourself needing to reverse the URL's name. With django-test-plus there is no need for the `from django.core.urlresolvers import reverse` boilerplate. Instead, use:

```python
def test_something(self):
    url = self.reverse('my-url-name')
    slug_url = self.reverse('name-takes-a-slug', slug='my-slug')
    pk_url = self.reverse('name-takes-a-pk', pk=12)
```

As you can see our reverse also passes along any args or kwargs you need
to pass in.

## `get(url_name, follow=True, *args, **kwargs)`

Another thing you do often is HTTP get urls. Our `get()` method
assumes you are passing in a named URL with any args or kwargs necessary
to reverse the url_name.
If needed, place kwargs for `TestClient.get()` in an 'extra' dictionary.:

```python
def test_get_named_url(self):
    response = self.get('my-url-name')
    # Get XML data via AJAX request
    xml_response = self.get(
        'my-url-name',
        extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
```

When using this get method two other things happen for you: we store the
last response in `self.last_response` and the response's Context in `self.context`.

So instead of:

```python
def test_default_django(self):
    response = self.client.get(reverse('my-url-name'))
    self.assertTrue('foo' in response.context)
    self.assertEqual(response.context['foo'], 12)
```

You can write:

```python
def test_testplus_get(self):
    self.get('my-url-name')
    self.assertInContext('foo')
    self.assertEqual(self.context['foo'], 12)
```

It's also smart about already reversed URLs, so you can be lazy and do:

```python
def test_testplus_get(self):
    url = self.reverse('my-url-name')
    self.get(url)
    self.response_200()
```

If you need to pass query string parameters to your url name, you can do so like this. Assuming the name 'search' maps to '/search/' then:

```python
def test_testplus_get_query(self):
    self.get('search', data={'query': 'testing'})
```

Would GET `/search/?query=testing`.

## `post(url_name, data, follow=True, *args, **kwargs)`

Our `post()` method takes a named URL, an optional dictionary of data you wish
to post and any args or kwargs necessary to reverse the url_name.
If needed, place kwargs for `TestClient.post()` in an 'extra' dictionary.:

```python
def test_post_named_url(self):
    response = self.post('my-url-name', data={'coolness-factor': 11.0},
                         extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
```

*NOTE* Along with the frequently used get and post, we support all of the HTTP verbs such as put, patch, head, trace, options, and delete in the same fashion.

## `get_context(key)`

Often you need to get things out of the template context:

```python
def test_context_data(self):
    self.get('my-view-with-some-context')
    slug = self.get_context('slug')
```

## `assertInContext(key)`

You can ensure a specific key exists in the last response's context by
using:

```python
def test_in_context(self):
    self.get('my-view-with-some-context')
    self.assertInContext('some-key')
```

## `assertContext(key, value)`

We can get context values and ensure they exist, but we can also test
equality while we're at it. This asserts that key == value:

```python
def test_in_context(self):
    self.get('my-view-with-some-context')
    self.assertContext('some-key', 'expected value')
```

## Response Testing Helper Methods

### `assertResponseContains(text, response=None, html=True, **kwargs)`

Convenience wrapper for Django's `assertContains` method. Tests that the response contains the given text:

```python
def test_response_contains(self):
    self.get('my-view')
    self.assertResponseContains('Welcome to my site')
    
    # Or with explicit response
    response = self.get('my-view')
    self.assertResponseContains('Welcome to my site', response)
```

### `assertResponseNotContains(text, response=None, html=True, **kwargs)`

Convenience wrapper for Django's `assertNotContains` method. Tests that the response does not contain the given text:

```python
def test_response_not_contains(self):
    self.get('my-view')
    self.assertResponseNotContains('Secret admin content')
```

### `assertResponseHeaders(headers, response=None)`

Check that the headers in the response are as expected. Only headers defined in the `headers` parameter are compared, other keys present on the response will be ignored:

```python
def test_response_headers(self):
    self.get('my-api-view')
    self.assertResponseHeaders({
        'Content-Type': 'application/json',
        'X-Custom-Header': 'my-value'
    })
    
    # Or with explicit response
    response = self.get('my-api-view')
    self.assertResponseHeaders({
        'Content-Type': 'application/json'
    }, response)
```

## `assert_http_###_<status_name>(response, msg=None)` - status code checking

Another test you often need to do is check that a response has a certain
HTTP status code. With Django's default TestCase you would write:

```python
from django.core.urlresolvers import reverse

def test_status(self):
    response = self.client.get(reverse('my-url-name'))
    self.assertEqual(response.status_code, 200)
```

With django-test-plus you can shorten that to be:

```python
def test_better_status(self):
    response = self.get('my-url-name')
    self.assert_http_200_ok(response)
```

Django-test-plus provides **62 different HTTP status code assertions** covering the complete range of standard HTTP status codes. The status assertions can be found in their own [mixin](https://github.com/revsys/django-test-plus/blob/main/test_plus/status_codes.py) and should be searchable if you're using an IDE like PyCharm.

Each of the assertion methods takes an optional Django test client `response` and a string `msg` argument that, if specified, is used as the error message when a failure occurs. The methods `assert_http_301_moved_permanently` and `assert_http_302_found` also take an optional `url` argument that if passed, will check to make sure the `response.url` matches.

If it's available, the `assert_http_###_<status_name>` methods will use the last response. So you can do:

```python
def test_status(self):
    self.get('my-url-name')
    self.assert_http_200_ok()
```

Which is a bit shorter.

### Available HTTP Status Code Assertions

**Informational (1xx):**
- `assert_http_100_continue()`
- `assert_http_101_switching_protocols()`

**Successful (2xx):**
- `assert_http_200_ok()`
- `assert_http_201_created()`
- `assert_http_202_accepted()`
- `assert_http_203_non_authoritative_information()`
- `assert_http_204_no_content()`
- `assert_http_205_reset_content()`
- `assert_http_206_partial_content()`
- `assert_http_207_multi_status()`
- `assert_http_208_already_reported()`
- `assert_http_226_im_used()`

**Redirection (3xx):**
- `assert_http_300_multiple_choices()`
- `assert_http_301_moved_permanently(url=None)` - takes optional `url` parameter
- `assert_http_302_found(url=None)` - takes optional `url` parameter
- `assert_http_303_see_other()`
- `assert_http_304_not_modified()`
- `assert_http_305_use_proxy()`
- `assert_http_306_reserved()`
- `assert_http_307_temporary_redirect()`
- `assert_http_308_permanent_redirect()`

**Client Error (4xx):**
- `assert_http_400_bad_request()`
- `assert_http_401_unauthorized()`
- `assert_http_402_payment_required()`
- `assert_http_403_forbidden()`
- `assert_http_404_not_found()`
- `assert_http_405_method_not_allowed()`
- `assert_http_406_not_acceptable()`
- `assert_http_407_proxy_authentication_required()`
- `assert_http_408_request_timeout()`
- `assert_http_409_conflict()`
- `assert_http_410_gone()`
- `assert_http_411_length_required()`
- `assert_http_412_precondition_failed()`
- `assert_http_413_request_entity_too_large()`
- `assert_http_414_request_uri_too_long()`
- `assert_http_415_unsupported_media_type()`
- `assert_http_416_requested_range_not_satisfiable()`
- `assert_http_417_expectation_failed()`
- `assert_http_422_unprocessable_entity()`
- `assert_http_423_locked()`
- `assert_http_424_failed_dependency()`
- `assert_http_426_upgrade_required()`
- `assert_http_428_precondition_required()`
- `assert_http_429_too_many_requests()`
- `assert_http_431_request_header_fields_too_large()`
- `assert_http_451_unavailable_for_legal_reasons()`

**Server Error (5xx):**
- `assert_http_500_internal_server_error()`
- `assert_http_501_not_implemented()`
- `assert_http_502_bad_gateway()`
- `assert_http_503_service_unavailable()`
- `assert_http_504_gateway_timeout()`
- `assert_http_505_http_version_not_supported()`
- `assert_http_506_variant_also_negotiates()`
- `assert_http_507_insufficient_storage()`
- `assert_http_508_loop_detected()`
- `assert_http_509_bandwidth_limit_exceeded()`
- `assert_http_510_not_extended()`
- `assert_http_511_network_authentication_required()`

The `response_###()` methods that are deprecated, but still available for use, include:

- `response_200()`
- `response_201()`
- `response_204()`
- `response_301()`
- `response_302()`
- `response_400()`
- `response_401()`
- `response_403()`
- `response_404()`
- `response_405()`
- `response_409()`
- `response_410()`

All of which take an optional Django test client response and a str msg argument that, if specified, is used as the error message when a failure occurs. Just like the `assert_http_###_<status_name>()` methods, these methods will use the last response if it's available.

## `get_check_200(url_name, *args, **kwargs)`

GETing and checking views return status 200 is a common test. This method makes it more convenient::

```python
def test_even_better_status(self):
    response = self.get_check_200('my-url-name')
```

## make_user(username='testuser', password='password', perms=None)

When testing out views you often need to create various users to ensure
all of your logic is safe and sound. To make this process easier, this
method will create a user for you:

```python
def test_user_stuff(self)
    user1 = self.make_user('u1')
    user2 = self.make_user('u2')
```

### Advanced Features

#### **Automatic Email Generation**
The method automatically generates email addresses using the format `{username}@example.com`:

```python
def test_user_email(self):
    user = self.make_user('john')
    # user.email will be 'john@example.com'
    self.assertEqual(user.email, 'john@example.com')
```

#### **Custom User Model Support**
The method works with custom user models by detecting the `USERNAME_FIELD` and `EMAIL_FIELD` attributes:

```python
# Works with custom user models that use email as username
class CustomUserModel(AbstractUser):
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
```

#### **Complex Permission Handling**
You can pass in user permissions using either specific permission names or wildcard patterns:

```python
def test_user_permissions(self):
    # Specific permission
    user1 = self.make_user('user1', perms=['myapp.add_widget'])
    
    # Multiple specific permissions
    user2 = self.make_user('user2', perms=[
        'myapp.add_widget',
        'myapp.change_widget',
        'otherapp.view_model'
    ])
    
    # Wildcard permissions (all permissions for an app)
    admin_user = self.make_user('admin', perms=['myapp.*'])
    
    # Mix of specific and wildcard permissions
    power_user = self.make_user('power', perms=[
        'myapp.*',
        'otherapp.view_model'
    ])
```

#### **Factory Boy Integration**
If creating a User in your project is more complicated, say for example
you removed the `username` field from the default Django Auth model,
you can provide a [Factory
Boy](https://factoryboy.readthedocs.org/en/latest/) factory to create
it or override this method on your own sub-class.

To use a Factory Boy factory, create your class like this::

```python
from test_plus.test import TestCase
from .factories import UserFactory


class MySpecialTest(TestCase):
    user_factory = UserFactory

    def test_special_creation(self):
        user1 = self.make_user('u1')
```

**NOTE:** Users created by this method will have their password
set to the string 'password' by default, in order to ease testing.
If you need a specific password, override the `password` parameter.

**NOTE:** When using Factory Boy, automatic email generation is disabled 
and the factory is responsible for setting all user fields.

## `print_form_errors(response_or_form=None)`

When debugging a failing test for a view with a form, this method helps you
quickly look at any form errors.

Example usage:

```python
class MyFormTest(TestCase):

    self.post('my-url-name', data={})
    self.print_form_errors()

    # or

    resp = self.post('my-url-name', data={})
    self.print_form_errors(resp)

    # or

    form = MyForm(data={})
    self.print_form_errors(form)
```

## Authentication Helpers

### `assertLoginRequired(url_name, *args, **kwargs)`

This method helps you test that a given named URL requires authorization:

```python
def test_auth(self):
    self.assertLoginRequired('my-restricted-url')
    self.assertLoginRequired('my-restricted-object', pk=12)
    self.assertLoginRequired('my-restricted-object', slug='something')
```

### `login()` context

Along with ensuring a view requires login and creating users, the next
thing you end up doing is logging in as various users to test your
restriction logic:

```python
def test_restrictions(self):
    user1 = self.make_user('u1')
    user2 = self.make_user('u2')

    self.assertLoginRequired('my-protected-view')

    with self.login(username=user1.username, password='password'):
        response = self.get('my-protected-view')
        # Test user1 sees what they should be seeing

    with self.login(username=user2.username, password='password'):
        response = self.get('my-protected-view')
        # Test user2 see what they should be seeing
```

Since we're likely creating our users using `make_user()` from above,
the login context assumes the password is 'password' unless specified
otherwise. Therefore you you can do:

```python
def test_restrictions(self):
    user1 = self.make_user('u1')

    with self.login(username=user1.username):
        response = self.get('my-protected-view')
```

We can also derive the username if we're using `make_user()` so we can
shorten that up even further like this:

```python
def test_restrictions(self):
    user1 = self.make_user('u1')

    with self.login(user1):
        response = self.get('my-protected-view')
```

## Ensuring low query counts

### `assertNumQueriesLessThan(number)` - context

Django provides
[`assertNumQueries`](https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries)
which is great when your code generates a specific number of
queries. However, if this number varies due to the nature of your data, with
this method you can still test to ensure the code doesn't start producing a ton
more queries than you expect:

```python
def test_something_out(self):

    with self.assertNumQueriesLessThan(7):
        self.get('some-view-with-6-queries')
```

### `assertGoodView(url_name, *args, **kwargs)`

This method does a few things for you. It:

- Retrieves the name URL
- Ensures the view does not generate more than 50 queries
- Ensures the response has status code 200
- Returns the response

Often a wide, sweeping test like this is better than no test at all. You
can use it like this:

```python
def test_better_than_nothing(self):
    response = self.assertGoodView('my-url-name')
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
        self.assert_http_200_ok()
```

Note that using `APITestCase` requires Django >= 1.8 and having installed `django-rest-framework`.

## Testing class-based "generic" views

The TestCase methods `get()` and `post()` work for both function-based
and class-based views. However, in doing so they invoke Django's
URL resolution, middleware, template processing, and decorator systems.
For integration testing this is desirable, as you want to ensure your
URLs resolve properly, view permissions are enforced, etc.
For unit testing this is costly because all these Django request/response
systems are invoked in addition to your method, and they typically do not
affect the end result.

Class-based views (derived from Django's `generic.models.View` class)
contain methods and mixins which makes granular unit testing (more) feasible.
Quite often your usage of a generic view class comprises an override
of an existing method. Invoking the entire view and the Django request/response
stack is a waste of time when you really want to call the overridden
method directly and test the result.

CBVTestCase to the rescue!

As with TestCase above, have your tests inherit
from test_plus.test.CBVTestCase rather than TestCase like so:

```python
from test_plus.test import CBVTestCase

class MyViewTests(CBVTestCase):
```

## Methods

### `get_instance(cls, initkwargs=None, request=None, *args, **kwargs)`

This core method simplifies the instantiation of your class, giving you
a way to invoke class methods directly.

Returns an instance of `cls`, initialized with `initkwargs`.
Sets `request`, `args`, and `kwargs` attributes on the class instance.
`args` and `kwargs` are the same values you would pass to `reverse()`.

Sample usage:

```python
from django.views import generic
from test_plus.test import CBVTestCase

class MyClass(generic.DetailView)

    def get_context_data(self, **kwargs):
        kwargs['answer'] = 42
        return kwargs

class MyTests(CBVTestCase):

    def test_context_data(self):
        my_view = self.get_instance(MyClass, {'object': some_object})
        context = my_view.get_context_data()
        self.assertEqual(context['answer'], 42)
```

### `get(cls, initkwargs=None, *args, **kwargs)`

Invokes `cls.get()` and returns the response, rendering template if possible.
Builds on the `CBVTestCase.get_instance()` foundation.

All test_plus.test.TestCase methods are valid, so the following works:

```python
response = self.get(MyClass)
self.assertContext('my_key', expected_value)
```

All test_plus TestCase side-effects are honored and all test_plus
TestCase assertion methods work with `CBVTestCase.get()`.

**NOTE:** This method bypasses Django's middleware, and therefore context
variables created by middleware are not available. If this affects your
template/context testing, you should use TestCase instead of CBVTestCase.

### `post(cls, data=None, initkwargs=None, *args, **kwargs)`

Invokes `cls.post()` and returns the response, rendering template if possible.
Builds on the `CBVTestCase.get_instance()` foundation.

Example:

```python
response = self.post(MyClass, data={'search_term': 'revsys'})
self.response_200(response)
self.assertContext('company_name', 'RevSys')
```

All test_plus TestCase side-effects are honored and all test_plus
TestCase assertion methods work with `CBVTestCase.post()`.

**NOTE:** This method bypasses Django's middleware, and therefore context
variables created by middleware are not available. If this affects your
template/context testing you should use TestCase instead of CBVTestCase.

### `get_check_200(cls, initkwargs=None, *args, **kwargs)`

Works just like `TestCase.get_check_200()`.
Caller must provide a view class instead of a URL name or path parameter.

All test_plus TestCase side-effects are honored and all test_plus
TestCase assertion methods work with `CBVTestCase.post()`.

### `assertGoodView(cls, initkwargs=None, *args, **kwargs)`

Works just like `TestCase.assertGoodView()`.
Caller must provide a view class instead of a URL name or path parameter.

All test_plus TestCase side-effects are honored and all test_plus
TestCase assertion methods work with `CBVTestCase.post()`.

## NoLoggingRunner Test Runner

Django-test-plus includes a custom test runner that disables logging during tests to reduce noise and improve performance. This is particularly useful when your application has extensive logging that clutters test output.

### Usage

To use the NoLoggingRunner, update your Django settings:

```python
# settings.py
TEST_RUNNER = 'test_plus.runner.NoLoggingRunner'
```

### How it works

The NoLoggingRunner extends Django's default `DiscoverRunner` and disables all logging below the CRITICAL level during test execution. This means:

- DEBUG, INFO, WARNING, and ERROR log messages are suppressed
- CRITICAL log messages will still appear
- Logging is only disabled during test runs, not in your actual application

### When to use

Consider using NoLoggingRunner when:

- Your tests produce excessive log output that makes it hard to read test results
- You want to improve test performance by reducing I/O operations
- You're running tests in CI/CD environments where log output isn't needed
- You have many tests and want cleaner output

### Alternative usage

You can also use it selectively by importing and using it directly:

```python
# In your test configuration
from test_plus.runner import NoLoggingRunner

# Use it as needed
runner = NoLoggingRunner()
```

## Development

To work on django-test-plus itself, clone this repository and run the following command:

```shell
$ pip install -e .
$ pip install -e .[test]
```

### Testing with Nox

Django-test-plus uses [Nox](https://nox.thea.codes/) to test against multiple Python and Django version combinations. This ensures compatibility across the supported matrix.

#### Version Matrix

The project tests against:

**Python versions:** 3.9, 3.10, 3.11, 3.12, 3.13
**Django versions:** 4.2 LTS, 5.1, 5.2 LTS  
**Django REST Framework versions:** 3.14, 3.15, 3.16

**Note:** Python 3.9 is not compatible with Django 5.1+ and those combinations are automatically skipped.

#### Running Tests

```shell
# Run all tests across all Python/Django combinations
$ nox

# Run tests for all Python versions with latest Django
$ nox -s tests

# Run tests with Django REST Framework
$ nox -s tests_drf

# Run tests for specific Python version
$ nox -s tests-3.11

# Run tests for specific Django version
$ nox -s tests --django=4.2

# Run with pytest arguments
$ nox -s tests -- -v --tb=short

# List all available sessions
$ nox -l
```

#### Session Details

- **tests**: Runs the standard test suite against Django without DRF
- **tests_drf**: Runs tests with Django REST Framework installed
- Sessions use `uv` for faster virtual environment creation when available
- Virtual environments are reused by default for faster subsequent runs

#### Local Development

For local development, you can also run tests directly with pytest:

```shell
# Run tests with current environment (uses pytest.ini config)
$ pytest

# Run tests reusing database (faster for development)
$ pytest --reuse-db

# Run specific test file
$ pytest test_project/test_app/tests/test_unittests.py

# Run specific test method
$ pytest test_project/test_app/tests/test_unittests.py::TestCasePlusTests::test_get
```

**NOTE**: You will also need to ensure that the `test_project` directory, located
at the root of this repo, is in your virtualenv's path.

## Keep in touch!

If you have a question about this project, please open a GitHub issue. If you love us and want to keep track of our goings-on, here's where you can find us online:

<a href="https://revsys.com?utm_medium=github&utm_source=django-test-plus"><img src="https://pbs.twimg.com/profile_images/915928618840285185/sUdRGIn1_400x400.jpg" height="50" /></a>
<a href="https://twitter.com/revsys"><img src="https://cdn1.iconfinder.com/data/icons/new_twitter_icon/256/bird_twitter_new_simple.png" height="43" /></a>
<a href="https://www.facebook.com/revsysllc/"><img src="https://cdn3.iconfinder.com/data/icons/picons-social/57/06-facebook-512.png" height="50" /></a>
