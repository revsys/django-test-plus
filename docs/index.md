# Overview

[![PyPI](https://img.shields.io/pypi/v/django-test-plus.svg)](https://pypi.org/project/django-test-plus/)
[![Python versions](https://img.shields.io/pypi/pyversions/django-test-plus.svg)](https://pypi.org/project/django-test-plus/)
[![Django versions](https://img.shields.io/pypi/frameworkversions/django/django-test-plus.svg)](https://pypi.org/project/django-test-plus/)

> Useful additions to Django's default TestCase, from [REVSYS](https://www.revsys.com/).

Let's face it, writing tests isn't always fun. Part of the reason for that is all
of the boilerplate you end up writing. django-test-plus is an attempt to cut down
on some of that when writing Django tests. We guarantee it will increase the time
before you get carpal tunnel by at least 3 weeks!

If you would like to get started testing your Django apps, or improve how your
team is testing, we offer [TestStart](https://www.revsys.com/teststart/) to help
your team dramatically improve your productivity.

## Why use django-test-plus?

It is additive. `test_plus.test.TestCase` subclasses Django's, so everything you
already know still works and you can adopt the helpers one at a time.

- **Reverse URLs inline.** `self.get('my-url-name')` instead of importing
  `reverse` and threading it through every call. Args and kwargs pass straight
  through, and an already-reversed URL works too.
- **Assert on status codes readably.** `self.assert_http_200_ok()` rather than
  `self.assertEqual(response.status_code, 200)`, for
  [most of the status codes](methods.md).
- **Skip the response variable.** The last response and its context are stored
  for you, so the assertion helpers default to them.
- **Create users without ceremony.** [`make_user()`](methods.md) builds one with
  a sensible username, email, and password, takes a permission list, and honours a
  factory-boy factory if your User model needs one.
- **Check authentication in a line.** [`assertLoginRequired()`](auth_helpers.md)
  for any URL and HTTP method, plus a [`login()`](auth_helpers.md) context
  manager for testing what each user should see.
- **Keep query counts honest.** [`assertNumQueriesLessThan()`](low_query_counts.md)
  and [`assertGoodView()`](low_query_counts.md) catch N+1 regressions without
  pinning an exact number that churns on every change.
- **Unit test class-based views directly.** [`CBVTestCase`](cbvtestcase.md)
  invokes a view's methods without the URL resolution, middleware, and template
  stack, when that machinery is not what you are testing.
- **Works with unittest, pytest, and DRF.** The same helpers, three ways.
  See below.

Maintained by [REVSYS](https://www.revsys.com/), who have been building and
maintaining Django projects since before 1.0.

## Installation

```shell
pip install django-test-plus
```

## Support

- Python 3.10, 3.11, 3.12, 3.13, and 3.14, including the 3.14 free-threaded build (3.14t)
- Django 4.2 LTS, 5.1, 5.2 LTS, 6.0, and 6.1

## The same test, three ways

The helpers are identical whichever style you write in.

### unittest

Inherit from `test_plus.test.TestCase` rather than the normal
`django.test.TestCase`:

```python
from test_plus.test import TestCase

class MyViewTests(TestCase):

    def test_the_view(self):
        self.get('my-url-name')
        self.response_200()
        self.assertResponseContains('<p>Hello, World!</p>')
```

### pytest

Ask for the `tp` fixture and every method above is available on it:

```python
def test_the_view(tp):
    tp.get('my-url-name')
    tp.response_200()
    tp.assertResponseContains('<p>Hello, World!</p>')
```

### pytest with Django REST Framework

`tp_api` is the same thing backed by DRF's `APIClient`, so you can post JSON and
assert on the result:

```python
def test_the_api(tp_api):
    response = tp_api.post('my-api-view', extra={'format': 'json'})
    assert response.status_code == 200
```

Anything that touches the database needs pytest-django's `db` fixture alongside
`tp`. That covers `make_user()`, the `login()` context, and the query counting
helpers. See [pytest usage](usage.md#pytest-usage) for the details.

## Where to next

- [Usage](usage.md): the pytest fixtures and testing DRF views
- [Methods](methods.md): requests, status assertions, response, and context helpers
- [Authentication helpers](auth_helpers.md): `assertLoginRequired` and the `login()` context
- [Ensuring low query counts](low_query_counts.md): `assertNumQueriesLessThan` and `assertGoodView`
- [Testing class-based views](cbvtestcase.md)
- [Disable logging](disable_logging.md)
- [API reference](reference.md)

## llms.txt

This documentation is available in the [llms.txt](https://llmstxt.org/) format, a
Markdown convention suited to LLMs and AI coding assistants.

Two files are published:

- [`llms.txt`](https://django-test-plus.readthedocs.io/en/latest/llms.txt): a
  short description of the project plus links to each section of the
  documentation. The structure is described [here](https://llmstxt.org/#format).
- [`llms-full.txt`](https://django-test-plus.readthedocs.io/en/latest/llms-full.txt):
  the same index with the content of every page included inline, including the
  generated API reference.

Every page is also published as Markdown alongside its HTML, so you can link an
assistant at a single section rather than the whole corpus. Append `.md` to the
page name:

```text
https://django-test-plus.readthedocs.io/en/latest/usage.md
https://django-test-plus.readthedocs.io/en/latest/methods.md
https://django-test-plus.readthedocs.io/en/latest/reference.md
```

These files are not picked up automatically by IDEs or coding agents today, but
most will use them if you supply a link or paste the text.
