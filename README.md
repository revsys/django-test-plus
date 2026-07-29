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

- Python 3.10, 3.11, 3.12, 3.13, and 3.14, including the 3.14 free-threaded
  build (3.14t).

- Django 4.2 LTS, 5.1, 5.2 LTS, 6.0, and 6.1.

## Installation

```shell
$ pip install django-test-plus
```

## Usage

Have your tests inherit from `test_plus.test.TestCase` rather than the normal
`django.test.TestCase`:

```python
from test_plus.test import TestCase

class MyViewTests(TestCase):
    ...
```

That is enough to get rolling. Here is a taste of what you get — reversing
URLs, checking status codes, and inspecting context without the boilerplate:

```python
class MyViewTests(TestCase):

    def test_the_view(self):
        # GET a named URL, with args or kwargs if it needs them
        self.get('my-url-name')
        self.response_200()

        # The last response and its context are stored for you
        self.assertInContext('some-key')
        self.assertResponseContains('<p>Hello, World!</p>')

        # POST data, then check the redirect
        self.post('my-form-view', data={'name': 'Test'})
        self.response_302()

    def test_auth(self):
        user = self.make_user('u1')

        self.assertLoginRequired('my-protected-view')

        with self.login(user):
            self.get_check_200('my-protected-view')

    def test_query_count(self):
        # 200 OK in under 50 queries, in one line
        self.assertGoodView('my-url-name')
```

You are encouraged to create *your own* sub-class for your project so you can
add project-specific helper methods:

```python
# myproject/test.py
from test_plus.test import TestCase as PlusTestCase

class TestCase(PlusTestCase):
    pass
```

There is a pytest fixture too — ask for `tp` and you get the same helpers:

```python
def test_url_reverse(tp):
    assert tp.reverse('api') == '/api/'
```

## Documentation

**Full documentation, including the complete method reference, is available at
[django-test-plus.readthedocs.org](http://django-test-plus.readthedocs.org).**

- [Usage](https://django-test-plus.readthedocs.io/en/latest/usage.html) —
  including pytest fixtures and testing DRF views
- [Methods](https://django-test-plus.readthedocs.io/en/latest/methods.html) —
  requests, status code assertions, response and context helpers, `make_user`
- [Authentication helpers](https://django-test-plus.readthedocs.io/en/latest/auth_helpers.html) —
  `assertLoginRequired` and the `login()` context
- [Ensuring low query counts](https://django-test-plus.readthedocs.io/en/latest/low_query_counts.html) —
  `assertNumQueriesLessThan` and `assertGoodView`
- [Testing class-based views](https://django-test-plus.readthedocs.io/en/latest/cbvtestcase.html)
- [Disable logging](https://django-test-plus.readthedocs.io/en/latest/disable_logging.html)

## Development

To work on django-test-plus itself, clone this repository and run the following command:

```shell
$ pip install -e .
$ pip install -e .[test]
```

## To run all tests:

```shell
$ nox
```

**NOTE**: You will also need to ensure that the `test_project` directory, located
at the root of this repo, is in your virtualenv's path.

## Keep in touch!

If you have a question about this project, please open a GitHub issue. If you love us and want to keep track of our goings-on, here's where you can find us online:

<a href="https://revsys.com?utm_medium=github&utm_source=django-test-plus"><img src="https://pbs.twimg.com/profile_images/915928618840285185/sUdRGIn1_400x400.jpg" height="50" /></a>
<a href="https://twitter.com/revsys"><img src="https://cdn1.iconfinder.com/data/icons/new_twitter_icon/256/bird_twitter_new_simple.png" height="43" /></a>
<a href="https://www.facebook.com/revsysllc/"><img src="https://cdn3.iconfinder.com/data/icons/picons-social/57/06-facebook-512.png" height="50" /></a>
