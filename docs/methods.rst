Methods
-------

reverse(url\_name, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When testing views you often find yourself needing to reverse the URL's name. With django-test-plus there is no need for the ``from django.core.urlresolvers import reversee`` boilerplate. Instead just use::

    def test_something(self):
        url = self.reverse('my-url-name')
        slug_url = self.reverse('name-takes-a-slug', slug='my-slug')
        pk_url = self.reverse('name-takes-a-pk', pk=12)

As you can see our reverse also passes along any args or kwargs you need
to pass in.

get(url\_name, follow=True, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another thing you do often is HTTP get urls. Our ``get()`` method
assumes you are passing in a named URL with any args or kwargs necessary
to reverse the url\_name.
If needed, place kwargs for ``TestClient.get()`` in an 'extra' dictionary.::

    def test_get_named_url(self):
        response = self.get('my-url-name')
        # Get XML data via AJAX request
        xml_response = self.get(
            'my-url-name',
            extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

When using this get method two other things happen for you, we store the
last response in ``self.last\_response`` and the response's Context in ``self.context``.
So instead of::

    def test_default_django(self):
        response = self.client.get(reverse('my-url-name'))
        self.assertTrue('foo' in response.context)
        self.assertEqual(response.context['foo'], 12)

You can instead write::

    def test_testplus_get(self):
        self.get('my-url-name')
        self.assertInContext('foo')
        self.assertEqual(self.context['foo'], 12)

It's also smart about already reversed URLs so you can be lazy and do::

    def test_testplus_get(self):
        url = self.reverse('my-url-name')
        self.get(url)
        self.response_200()

If you need to pass query string parameters to your url name, you can do so like this. Assuming the name 'search' maps to '/search/' then::

    def test_testplus_get_query(self):
        self.get('search', data={'query': 'testing'})

Would GET /search/?query=testing

post(url\_name, data, follow=True, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our ``post()`` method takes a named URL, the dictionary of data you wish
to post and any args or kwargs necessary to reverse the url\_name.
If needed, place kwargs for ``TestClient.post()`` in an 'extra' dictionary.::

    def test_post_named_url(self):
        response = self.post('my-url-name', data={'coolness-factor': 11.0},
                             extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

get_context(key)
~~~~~~~~~~~~~~~~

Often you need to get things out of the template context, so let's make that
easy::

    def test_context_data(self):
        self.get('my-view-with-some-context')
        slug = self.get_context('slug')

assertInContext(key)
~~~~~~~~~~~~~~~~~~~~

You can ensure a specific key exists in the last response's context by
using::

    def test_in_context(self):
        self.get('my-view-with-some-context')
        self.assertInContext('some-key')

assertContext(key, value)
~~~~~~~~~~~~~~~~~~~~~~~~~

We can get context values and ensure they exist, but so let's also test
equality while we're at it. This asserts that key == value::

    def test_in_context(self):
        self.get('my-view-with-some-context')
        self.assertContext('some-key', 'expected value')

response\_XXX(response) - status code checking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Another test you often need to do is check that a response has a certain
HTTP status code. With Django's default TestCase you would write::

    from django.core.urlresolvers import reverse

    def test_status(self):
        response = self.client.get(reverse('my-url-name'))
        self.assertEqual(response.status_code, 200)

With django-test-plus you can shorten that to be::

    def test_better_status(self):
        response = self.get('my-url-name')
        self.response_200(response)

django-test-plus provides the following response method checks for you::

    - response_200()
    - response_201()
    - response_302()
    - response_403()
    - response_404()

All of which take an option Django test client response as their only argument.
If it's available, the response_XXX methods will use the last response. So you
can do::

    def test_status(self):
        self.get('my-url-name')
        self.response_200()

Which is a bit shorter.

get\_check\_200(url\_name, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

GETing and checking views return status 200 is so common a test this
method makes it even easier::

    def test_even_better_status(self):
        response = self.get_check_200('my-url-name')

make\_user(username='testuser', password='password', perms=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When testing out views you often need to create various users to ensure
all of your logic is safe and sound. To make this process easier, this
method will create a user for you::

    def test_user_stuff(self)
        user1 = self.make_user('u1')
        user2 = self.make_user('u2')

**NOTE:** This work properly with version of Django prior to 1.6 and
will use your own User class if you have created your own User model.

If creating a User in your project is more complicated, say for example
you removed the ``username`` field from the default Django Auth model
you can provide a `Factory
Boy <https://factoryboy.readthedocs.org/en/latest/>`__ factory to create
it or simply override this method on your own sub-class.

To use a Factory Boy factory simply create your class like this::

    from test_plus.test import TestCase
    from .factories import UserFactory


    class MySpecialTest(TestCase):
        user_factory = UserFactory

        def test_special_creation(self):
            user1 = self.make_user('u1')

**NOTE:** Users created by this method will have their password
set to the string 'password' by default, in order to ease testing.
If you need a specific password simply override the ``password`` parameter.

You can also pass in user permissions by passing in a string of
'``<app_name>.<perm name>``' or '``<app_name>.*``'.  For example::

    user2 = self.make_user(perms=['myapp.create_widget', 'otherapp.*'])
