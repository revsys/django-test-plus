Authentication Helpers
----------------------

assertLoginRequired(url\_name, \*args, method='get', \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method helps you test that a given named URL requires authorization::

    def test_auth(self):
        self.assertLoginRequired('my-restricted-url')
        self.assertLoginRequired('my-restricted-object', pk=12)
        self.assertLoginRequired('my-restricted-object', slug='something')

Like ``self.get()`` and friends, a plain URL works too when the name cannot be
reversed::

    def test_auth_by_url(self):
        self.assertLoginRequired('/restricted/')

Pass ``method`` to check a verb other than GET, which is useful for views that
only accept writes::

    def test_auth_on_post(self):
        self.assertLoginRequired('my-restricted-url', method='post')

``method`` accepts any verb supported by ``request()``: ``get``, ``post``,
``put``, ``patch``, ``head``, ``trace``, ``options``, and ``delete``.

login context
~~~~~~~~~~~~~

Along with ensuing a view requires login and creating users, the next
thing you end up doing is logging in as various users to test our your
restriction logic::

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

Since we're likely creating our users using ``make_user()`` from above,
the login context assumes the password is 'password' unless specified
otherwise. Therefore you you can do::

    def test_restrictions(self):
        user1 = self.make_user('u1')

        with self.login(username=user1.username):
            response = self.get('my-protected-view')

We can also derive the username if we're using ``make_user()`` so we can
shorten that up even further like this::

    def test_restrictions(self):
        user1 = self.make_user('u1')

        with self.login(user1):
            response = self.get('my-protected-view')
