# Methods

These examples are written in the unittest style, on a `TestCase` subclass. Every method here is also available on the pytest `tp` fixture. Write `tp.get('my-url-name')` where these read `self.get('my-url-name')`. See [pytest usage](usage.md#pytest-usage) for the details.

## reverse(url_name, \*args, \*\*kwargs)

When testing views you often find yourself needing to reverse the URL's name. With django-test-plus there is no need for the `from django.core.urlresolvers import reverse` boilerplate. Instead, use:

```python
def test_something(self):
    url = self.reverse('my-url-name')
    slug_url = self.reverse('name-takes-a-slug', slug='my-slug')
    pk_url = self.reverse('name-takes-a-pk', pk=12)
```

As you can see our reverse also passes along any args or kwargs you need to pass in.

## get(url_name, follow=False, \*args, \*\*kwargs)

Another thing you do often is HTTP get urls. Our `get()` method assumes you are passing in a named URL with any args or kwargs necessary to reverse the url_name. If needed, place kwargs for `TestClient.get()` in an 'extra' dictionary.:

```python
def test_get_named_url(self):
    response = self.get('my-url-name')
    # Get XML data via AJAX request
    xml_response = self.get(
        'my-url-name',
        extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
```

When using this get method two other things happen for you: we store the last response in `self.last\_response` and the response's Context in `self.context`. So instead of:

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

Would GET /search/?query=testing

## post(url_name, follow=False, \*args, \*\*kwargs)

Our `post()` method takes a named URL, an optional dictionary of data you wish to post and any args or kwargs necessary to reverse the url_name. If needed, place kwargs for `TestClient.post()` in an 'extra' dictionary.:

```python
def test_post_named_url(self):
    response = self.post('my-url-name', data={'coolness-factor': 11.0},
                         extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
```

## put(url_name, follow=False, \*args, \*\*kwargs)

To support all HTTP methods

## patch(url_name, follow=False, \*args, \*\*kwargs)

To support all HTTP methods

## head(url_name, follow=False, \*args, \*\*kwargs)

To support all HTTP methods

## trace(url_name, follow=False, \*args, \*\*kwargs)

To support all HTTP methods

## options(url_name, follow=False, \*args, \*\*kwargs)

To support all HTTP methods

## delete(url_name, follow=False, \*args, \*\*kwargs)

To support all HTTP methods

## get_context(key)

Often you need to get things out of the template context:

```python
def test_context_data(self):
    self.get('my-view-with-some-context')
    slug = self.get_context('slug')
```

## assertInContext(key)

You can ensure a specific key exists in the last response's context by using:

```python
def test_in_context(self):
    self.get('my-view-with-some-context')
    self.assertInContext('some-key')
```

## assertContext(key, value)

We can get context values and ensure they exist, but we can also test equality while we're at it. This asserts that key == value:

```python
def test_in_context(self):
    self.get('my-view-with-some-context')
    self.assertContext('some-key', 'expected value')
```

## assert_http_XXX\_\<status_name\>(response, msg=None) - status code checking

Another test you often need to do is check that a response has a certain HTTP status code. With Django's default TestCase you would write:

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

Django-test-plus provides an assertion for every status code documented in the [MDN HTTP status reference](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status), plus the non-standard 509. They live in their own [mixin](https://github.com/revsys/django-test-plus/blob/main/test_plus/status_codes.py), are listed in the [API reference](reference.md), and should be searchable if you're using an IDE like PyCharm. Earlier versions of django-test-plus used assertion methods in the pattern of `response_###()`. Those are still supported and are not going away, so there is no need to migrate existing tests. See below for a list of them.

Each of the assertion methods takes an optional Django test client `response` and a string `msg` argument that, if specified, is used as the error message when a failure occurs. The methods, `assert_http_301_moved_permanently` and `assert_http_302_found` also take an optional `url` argument that if passed, will check to make sure the `response.url` matches.

If it's available, the `assert_http_###_<status_name>` methods will use the last response. So you can do::

```python
def test_status(self):
    self.get('my-url-name')
    self.assert_http_200_ok()
```

Which is a bit shorter.

The `response_###()` methods, which remain fully supported, include:

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

## assertResponseContains(text, response=None, html=True)

You often want to check that the last response contains a chunk of HTML. With Django's default TestCase you would write:

```python
from django.core.urlresolvers import reverse

def test_response_contains(self):
    response = self.client.get(reverse('hello-world'))
    self.assertContains(response, '<p>Hello, World!</p>', html=True)
```

With django-test-plus you can shorten that to be:

```python
def test_response_contains(self):
    self.get('hello-world')
    self.assertResponseContains('<p>Hello, World!</p>')
```

## assertResponseNotContains(text, response=None, html=True)

The inverse of the above test, this method makes sure the last response does not include the chunk of HTML:

```python
def test_response_not_contains(self):
    self.get('hello-world')
    self.assertResponseNotContains('<p>Hello, Frank!</p>')
```

## assertResponseHeaders(headers, response=None)

Sometimes your views or middleware will set custom headers:

```python
def test_custom_headers(self):
    self.get('my-url-name')
    self.assertResponseHeaders({'X-Custom-Header': 'Foo'})
    self.assertResponseHeaders({'X-Does-Not-Exist': None})
```

You might also want to check standard headers:

```python
def test_content_type(self):
    self.get('my-json-view')
    self.assertResponseHeaders({'Content-Type': 'application/json'})
```

## assertResponseTemplateUsed(template_name, response=None)

You can check that a specific template was used to render the last response:

```python
def test_template_used(self):
    self.get('my-view')
    self.assertResponseTemplateUsed('my_template.html')
```

This is a convenience wrapper around Django's `assertTemplateUsed` that automatically uses `self.last_response` if no response is provided.

## assertResponseTemplateNotUsed(template_name, response=None)

You can check that a specific template was not used to render the last response:

```python
def test_template_not_used(self):
    self.get('my-view')
    self.assertResponseTemplateNotUsed('other_template.html')
```

This is a convenience wrapper around Django's `assertTemplateNotUsed` that automatically uses `self.last_response` if no response is provided.

## assertResponseMessages(expected_messages, response=None, ordered=True)

**Available in Django 5.0+**

Convenience wrapper for Django's `MessagesTestMixin.assertMessages` that uses `self.last_response` by default. For full details on the underlying assertion, see the [Django documentation on testing messages](https://docs.djangoproject.com/en/stable/ref/contrib/messages/#testing).

Example usage:

```python
from django.contrib.messages import Message
from django.contrib.messages.constants import SUCCESS, ERROR

def test_success_message(self):
    self.post('my-form-view', data={'name': 'Test'})
    expected_messages = [
        Message(level=SUCCESS, message='Form saved successfully!'),
    ]
    self.assertResponseMessages(expected_messages)

def test_multiple_messages(self):
    self.post('my-form-view', data={'invalid': 'data'})
    expected_messages = [
        Message(level=ERROR, message='Name is required.'),
        Message(level=ERROR, message='Email is required.'),
    ]
    self.assertResponseMessages(expected_messages)
```

For Django versions before 5.0, this method will raise a `NotImplementedError`. To skip tests conditionally:

```python
import unittest
import django

@unittest.skipIf(django.VERSION < (5, 0), "assertResponseMessages requires Django 5.0+")
def test_messages(self):
    self.get('view-with-messages')
    expected_messages = [Message(level=SUCCESS, message='Done!')]
    self.assertResponseMessages(expected_messages)
```

## get_check_200(url_name, \*args, \*\*kwargs)

GETing and checking views return status 200 is a common test. This method makes it more convenient:

```python
def test_even_better_status(self):
    response = self.get_check_200('my-url-name')
```

## assertRedirects(response, expected_url, ...) and assertURLEqual(url1, url2)

Both are Django's own assertions, re-exported so they are available on `TestCase` without an extra import.

`assertURLEqual` compares two URLs for equality, ignoring the ordering of query string parameters:

```python
def test_urls_match(self):
    self.assertURLEqual('/search/?a=1&b=2', '/search/?b=2&a=1')
```

## print_form_errors(response_or_form=None)

When debugging a failing test for a view with a form, this method helps you quickly look at any form errors. It accepts either a response or a form instance, and defaults to `self.last_response`:

```python
def test_form_errors(self):
    self.post('my-form-view', data={})
    self.print_form_errors()

def test_form_errors_explicit_response(self):
    resp = self.post('my-form-view', data={})
    self.print_form_errors(resp)

def test_form_errors_from_a_form(self):
    form = MyForm(data={})
    self.print_form_errors(form)
```

## make_user(username='testuser', password='password', perms=None)

When testing out views you often need to create various users to ensure all of your logic is safe and sound. To make this process easier, this method will create a user for you:

```python
def test_user_stuff(self)
    user1 = self.make_user('u1')
    user2 = self.make_user('u2')
```

If creating a User in your project is more complicated, say for example you removed the `username` field from the default Django Auth model, you can provide a [Factory Boy](https://factoryboy.readthedocs.org/en/latest/) factory to create it or override this method on your own sub-class.

To use a Factory Boy factory, create your class like this:

```python
from test_plus.test import TestCase
from .factories import UserFactory

class MySpecialTest(TestCase):
    user_factory = UserFactory

    def test_special_creation(self):
        user1 = self.make_user('u1')
```

**NOTE:** Users created by this method will have their password set to the string 'password' by default, in order to ease testing. If you need a specific password, override the `password` parameter.

You can also pass in user permissions by passing in a string of '`<app_name>.<perm name>`' or '`<app_name>.*`'. For example:

```python
user2 = self.make_user(perms=['myapp.create_widget', 'otherapp.*'])
```
