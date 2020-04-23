Testing class-based "generic" views
=====================================

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
Quite often usage of a generic view class comprises a simple method override.
Invoking the entire view and the Django request/response stack is a waste of
time... you really want to test the overridden method directly.

CBVTestCase to the rescue!

As with TestCase above, have your tests inherit
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

    class MyViewClass(generic.DetailView)

        def get_context_data(self, **kwargs):
            kwargs = super(MyViewClass, self).get_context_data(**kwargs)
            if hasattr(self.request, 'some_data'):
                kwargs.update({
                    'some_data': self.request.some_data
                })
            if hasattr(self, 'special_value'):
                kwargs.update({
                    'special_value': self.special_value
                })
            return kwargs

    class MyViewTests(CBVTestCase):

        def test_context_data(self):
            my_view = self.get_instance(MyViewClass, initkwargs={'special_value': 42})
            context = my_view.get_context_data()
            self.assertContext('special_value', 42)

        def test_request_attribute(self):
            request = django.test.RequestFactory().get('/')
            request.some_data = 5
            my_view = self.get_instance(MyViewClass, request=request)
            context = my_view.get_context_data()
            self.assertContext('some_data', 5)

get(cls, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Invokes ``cls.get()`` and returns the response, rendering template if possible.
Builds on the ``CBVTestCase.get_instance()`` foundation.

All test\_plus.test.TestCase methods are valid, so the following works::

    response = self.get(MyViewClass)
    self.assertContext('my_key', expected_value)

All test\_plus TestCase side-effects are honored and all test\_plus
TestCase assertion methods work with ``CBVTestCase.get()``.

If you need special request attributes, i.e. 'user', you can create a
custom Request with RequestFactory, assign to ``request.user``,
and use that in the ``get()``:

        def test_request_attribute(self):
            request = django.test.RequestFactory().get('/')
            request.user = some_user
            self.get(MyViewClass, request=request, pk=data.pk)
            self.assertContext('user', some_user)

**NOTE:** This method bypasses Django's middleware, and therefore context
variables created by middleware are not available. If this affects your
template/context testing you should use ``TestCase`` instead of ``CBVTestCase``.

post(cls, \*args, \*\*kwargs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Invokes ``cls.post()`` and returns the response, rendering template if possible.
Builds on the ``CBVTestCase.get_instance()`` foundation.

Example::

    response = self.post(MyViewClass, data={'search_term': 'revsys'})
    self.response_200(response)
    self.assertContext('company_name', 'RevSys')

All test\_plus TestCase side-effects are honored and all test\_plus
TestCase assertion methods work with ``CBVTestCase.post()``.

If you need special request attributes, i.e. 'user', you can create a
custom Request with RequestFactory, assign to ``request.user``,
and use that in the ``post()``:

        def test_request_attribute(self):
            request = django.test.RequestFactory().post('/')
            request.user = some_user
            self.post(MyViewClass, request=request, pk=self.data.pk, data={})
            self.assertContext('user', some_user)

**NOTE:** This method bypasses Django's middleware, and therefore context
variables created by middleware are not available. If this affects your
template/context testing you should use ``TestCase`` instead of ``CBVTestCase``.

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
