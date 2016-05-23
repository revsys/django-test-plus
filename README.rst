django-test-plus
================

Useful additions to Django's default TestCase from `Revolution
Systems <http://www.revsys.com/>`__

|travis ci status image| |Coverage Status|

Rationale
---------

Let's face it, writing tests isn't always fun. Part of the reason for
that is all of the boilerplate you end up writing. django-test-plus is
an attempt to cut down on some of that when writing Django tests. We
guarantee it will increase the time before you get carpal tunnel by at
least 3 weeks!

Support
-------

Supports: Python 2 and Python 3

Supports Django Versions: 1.5, 1.6, 1.7, 1.8, and 1.9

Documentation
--------------

Full documentation is available at http://django-test-plus.readthedocs.org

Usage
-----

Using django-test-plus is pretty easy, simply have your tests inherit
from test\_plus.test.TestCase rather than the normal
django.test.TestCase like so::

    from test_plus.test import TestCase

    class MyViewTests(TestCase):
        ...

This is sufficient to get things rolling, but you are encouraged to
create *your own* sub-class on a per project basis. This will allow you to add your own project specific helper methods.

For example, if you have a django project named 'myproject', you might
create the following in ``myproject/test.py``::

    from test_plus.test import TestCase as PlusTestCase

    class TestCase(PlusTestCase):
        pass

And then in your tests use::

    from myproject.test import TestCase

    class MyViewTests(TestCase):
        ...

Note that you can also option to import it like this if you want, which is
more similar to the regular importing of Django's TestCase::

    from test_plus import TestCase

Methods
-------

reverse(url\_name, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When testing views you often find yourself needing to reverse the URL's name. With django-test-plus there is no need for the ``from django.core.urlresolvers import reverse`` boilerplate. Instead just use::

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
    - response_405()

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

Authentication Helpers
----------------------

assertLoginRequired(url\_name, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's pretty easy to add a new view to a project and forget to restrict
it to be login required, this method helps make it easy to test that a
given named URL requires auth::

    def test_auth(self):
        self.assertLoginRequired('my-restricted-url')
        self.assertLoginRequired('my-restricted-object', pk=12)
        self.assertLoginRequired('my-restricted-object', slug='something')

login context
~~~~~~~~~~~~~

Along with ensuing a view requires login and creating users, the next
thing you end up doing is logging in as various users to test our your
restriction logic. This can be made easier with the following context::

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

Ensuring low query counts
-------------------------

assertNumQueriesLessThan(number) - context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Django provides
`assertNumQueries <https://docs.djangoproject.com/en/1.8/topics/testing/tools/#django.test.TransactionTestCase.assertNumQueries>`__
which is great when your code generates generates a specific number of
queries. However, if due to the nature of your data this number can vary
you often don't attempt to ensure the code doesn't start producing a ton
more queries than you expect::

    def test_something_out(self):

        with self.assertNumQueriesLessThan(7):
            self.get('some-view-with-6-queries')


**NOTE:** This isn't possible in versions of Django prior to 1.6, so the
context will run your code and assertions and issue a warning that it
cannot check the number of queries generated.

assertGoodView(url\_name, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method does a few of things for you, it:

    - Retrieves the name URL
    - Ensures the view does not generate more than 50 queries
    - Ensures the response has status code 200
    - Returns the response

Often a wide sweeping test like this is better than no test at all. You
can use it like this::

    def test_better_than_nothing(self):
        response = self.assertGoodView('my-url-name')

Testing class-based "generic" views
------------------------------------

The TestCase methods ``get()`` and ``post()`` work for both function-based
and class-based views. However, in doing so they invoke Django's
URL resolution, middleware, template processing, and decorator systems.
For integration testing this is desirable, as you want to ensure your
URLs resolve properly, view permissions are enforced, etc.
For unit testing this is costly because all these Django request/response
systems are invoked in addition to your method, and they typically do not
affect the end result.

Class-based views (derived from Django's ``generic.models.View`` class)
contain methods and mixins which makes granular unit testing (more) feasible.
Quite often your usage of a generic view class comprises a simple override
of an existing method. Invoking the entire view and the Django request/response
stack is a waste of time... you really want to call the overridden
method directly and test the result.

CBVTestCase to the rescue!

As with TestCase above, simply have your tests inherit
from test\_plus.test.CBVTestCase rather than TestCase like so::

    from test_plus.test import CBVTestCase

    class MyViewTests(CBVTestCase):

Methods
-------

get_instance(cls, initkwargs=None, request=None, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This core method simplifies the instantiation of your class, giving you
a way to invoke class methods directly.

Returns an instance of ``cls``, initialized with ``initkwargs``.
Sets ``request``, ``args``, and ``kwargs`` attributes on the class instance.
``args`` and ``kwargs`` are the same values you would pass to ``reverse()``.

Sample usage::

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

get(cls, initkwargs=None, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Invokes ``cls.get()`` and returns the response, rendering template if possible.
Builds on the ``CBVTestCase.get_instance()`` foundation.

All test\_plus.test.TestCase methods are valid, so the following works::

    response = self.get(MyClass)
    self.assertContext('my_key', expected_value)

All test\_plus TestCase side-effects are honored and all test\_plus
TestCase assertion methods work with ``CBVTestCase.get()``.

**NOTE:** This method bypasses Django's middleware, and therefore context
variables created by middleware are not available. If this affects your
template/context testing you should use TestCase instead of CBVTestCase.

post(cls, data=None, initkwargs=None, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Invokes ``cls.post()`` and returns the response, rendering template if possible.
Builds on the ``CBVTestCase.get_instance()`` foundation.

Example::

    response = self.post(MyClass, data={'search_term': 'revsys'})
    self.response_200(response)
    self.assertContext('company_name', 'RevSys')

All test\_plus TestCase side-effects are honored and all test\_plus
TestCase assertion methods work with ``CBVTestCase.post()``.

**NOTE:** This method bypasses Django's middleware, and therefore context
variables created by middleware are not available. If this affects your
template/context testing you should use TestCase instead of CBVTestCase.

get_check_200(cls, initkwargs=None, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Works just like ``TestCase.get_check_200()``.
Caller must provide a view class instead of a URL name or path parameter.

All test\_plus TestCase side-effects are honored and all test\_plus
TestCase assertion methods work with ``CBVTestCase.post()``.

assertGoodView(cls, initkwargs=None, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Works just like ``TestCase.assertGoodView()``.
Caller must provide a view class instead of a URL name or path parameter.

All test\_plus TestCase side-effects are honored and all test\_plus
TestCase assertion methods work with ``CBVTestCase.post()``.


.. |travis ci status image| image:: https://secure.travis-ci.org/revsys/django-test-plus.png
   :target: http://travis-ci.org/revsys/django-test-plus
.. |Coverage Status| image:: https://coveralls.io/repos/revsys/django-test-plus/badge.svg?branch=master
   :target: https://coveralls.io/r/revsys/django-test-plus?branch=master
