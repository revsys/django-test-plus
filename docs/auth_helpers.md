# Authentication Helpers

## assertLoginRequired(url_name, \*args, method='get', \*\*kwargs)

This method helps you test that a given named URL requires authorization:

```python
def test_auth(self):
    self.assertLoginRequired('my-restricted-url')
    self.assertLoginRequired('my-restricted-object', pk=12)
    self.assertLoginRequired('my-restricted-object', slug='something')
```

Like `self.get()` and friends, a plain URL works too when the name cannot be reversed:

```python
def test_auth_by_url(self):
    self.assertLoginRequired('/restricted/')
```

Pass `method` to check a verb other than GET, which is useful for views that only accept writes:

```python
def test_auth_on_post(self):
    self.assertLoginRequired('my-restricted-url', method='post')
```

`method` accepts any verb supported by `request()`: `get`, `post`, `put`, `patch`, `head`, `trace`, `options`, and `delete`.

The same thing with the pytest `tp` fixture (see [pytest usage](usage.md#pytest-usage)):

```python
def test_auth(tp):
    tp.assertLoginRequired('my-restricted-url')
    tp.assertLoginRequired('my-restricted-url', method='post')
```

## login context

Along with ensuing a view requires login and creating users, the next thing you end up doing is logging in as various users to test our your restriction logic:

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

Since we're likely creating our users using `make_user()` from above, the login context assumes the password is 'password' unless specified otherwise. Therefore you you can do:

```python
def test_restrictions(self):
    user1 = self.make_user('u1')

    with self.login(username=user1.username):
        response = self.get('my-protected-view')
```

We can also derive the username if we're using `make_user()` so we can shorten that up even further like this:

```python
def test_restrictions(self):
    user1 = self.make_user('u1')

    with self.login(user1):
        response = self.get('my-protected-view')
```

The login context works the same way on the pytest `tp` fixture. Because `tp` does not set up database access on its own, ask for pytest-django's `db` fixture in any test that creates a user:

```python
def test_restrictions(tp, db):
    user1 = tp.make_user('u1')

    with tp.login(user1):
        response = tp.get('my-protected-view')
```
