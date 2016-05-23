import warnings

import django
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from django.shortcuts import resolve_url
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.models import Q
from distutils.version import LooseVersion
from django.test import RequestFactory, signals, TestCase as DjangoTestCase
from django.test.client import store_rendered_templates
from django.utils.functional import curry


class NoPreviousResponse(Exception):
    pass

# Build a real context in versions of Django greater than 1.6
# On versions below 1.6, create a context that simply warns that
# the query number assertion is not happening
if LooseVersion(django.get_version()) >= LooseVersion('1.6'):
    from django.test.utils import CaptureQueriesContext
    from django.contrib.auth import get_user_model

    User = get_user_model()

    CAPTURE = True

    class _AssertNumQueriesLessThanContext(CaptureQueriesContext):
        def __init__(self, test_case, num, connection):
            self.test_case = test_case
            self.num = num
            super(_AssertNumQueriesLessThanContext, self).__init__(connection)

        def __exit__(self, exc_type, exc_value, traceback):
            super(_AssertNumQueriesLessThanContext, self).__exit__(exc_type, exc_value, traceback)
            if exc_type is not None:
                return
            executed = len(self)
            self.test_case.assertTrue(
                executed < self.num, "%d queries executed, expected less than %d" % (
                    executed, self.num
                )
            )

else:
    from django.contrib.auth.models import User

    CAPTURE = False

    class _AssertNumQueriesLessThanContext(object):
        def __init__(self, test_case, num, connection):
            pass

        def __enter__(self):
            pass

        def __exit__(self, exc_type, exc_value, traceback):
            warnings.warn("assertNumQueriesLessThan being skipped, does not work prior to Django 1.6")


class login(object):
    """
    A useful login context for Django tests.  If the first argument is
    a User, we will login with that user's username.  If no password is
    given we will use 'password'.
    """
    def __init__(self, testcase, *args, **credentials):
        self.testcase = testcase

        if args and isinstance(args[0], User):
            USERNAME_FIELD = getattr(User, 'USERNAME_FIELD', 'username')
            credentials.update({
                USERNAME_FIELD: getattr(args[0], USERNAME_FIELD),
            })

        if not credentials.get('password', False):
            credentials['password'] = 'password'

        success = testcase.client.login(**credentials)
        self.testcase.assertTrue(
            success,
            "login failed with credentials=%r" % (credentials)
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()


class TestCase(DjangoTestCase):
    """
    Django TestCase with helpful additional features
    """
    user_factory = None

    def __init__(self, *args, **kwargs):
        self.last_response = None
        super(TestCase, self).__init__(*args, **kwargs)

    def tearDown(self):
        self.client.logout()

    def get(self, url_name, *args, **kwargs):
        """
        GET url by name using reverse()

        If reverse raises NoReverseMatch attempt to use it as a URL.
        """
        follow = kwargs.pop("follow", False)
        extra = kwargs.pop("extra", {})
        data = kwargs.pop("data", {})
        try:
            self.last_response = self.client.get(reverse(url_name, args=args, kwargs=kwargs), data=data, follow=follow, **extra)
        except NoReverseMatch:
            self.last_response = self.client.get(url_name, data=data, follow=follow, **extra)

        self.context = self.last_response.context
        return self.last_response

    def post(self, url_name, *args, **kwargs):
        """
        POST to url by name using reverse()

        If reverse raises NoReverseMatch attempt to use it as a URL.
        """
        follow = kwargs.pop("follow", False)
        data = kwargs.pop("data", None)
        extra = kwargs.pop("extra", {})
        try:
            self.last_response = self.client.post(reverse(url_name, args=args, kwargs=kwargs), data, follow=follow, **extra)
        except NoReverseMatch:
            self.last_response = self.client.post(url_name, data, follow=follow, **extra)

        return self.last_response

    def _which_response(self, response=None):
        if response is None and self.last_response is not None:
            return self.last_response
        else:
            return response

    def response_200(self, response=None):
        """ Given response has status_code 200 """
        response = self._which_response(response)
        self.assertEqual(response.status_code, 200)

    def response_201(self, response=None):
        """ Given response has status_code 201 """
        response = self._which_response(response)
        self.assertEqual(response.status_code, 201)

    def response_302(self, response=None):
        """ Given response has status_code 302 """
        response = self._which_response(response)
        self.assertEqual(response.status_code, 302)

    def response_401(self, response=None):
        """ Given response has status_code 401 """
        response = self._which_response(response)
        self.assertEqual(response.status_code, 401)

    def response_403(self, response=None):
        """ Given response has status_code 403 """
        response = self._which_response(response)
        self.assertEqual(response.status_code, 403)

    def response_404(self, response=None):
        """ Given response has status_code 404 """
        response = self._which_response(response)
        self.assertEqual(response.status_code, 404)

    def response_405(self, response=None):
        """ Given response has status_code 405 """
        response = self._which_response(response)
        self.assertEqual(response.status_code, 405)

    def response_410(self, response=None):
        """ Given response has status_code 410 """
        response = self._which_response(response)
        self.assertEqual(response.status_code, 410)

    def get_check_200(self, url, *args, **kwargs):
        """ Test that we can GET a page and it returns a 200 """
        response = self.get(url, *args, **kwargs)
        self.response_200(response)
        return response

    def assertLoginRequired(self, url, *args, **kwargs):
        """ Ensure login is required to GET this URL """
        response = self.get(url, *args, **kwargs)
        reversed_url = reverse(url, args=args, kwargs=kwargs)
        login_url = str(resolve_url(settings.LOGIN_URL))
        expected_url = "{0}?next={1}".format(login_url, reversed_url)
        self.assertRedirects(response, expected_url)

    def login(self, *args, **credentials):
        """ Login a user """
        return login(self, *args, **credentials)

    def reverse(self, name, *args, **kwargs):
        """ Reverse a url, convenience to avoid having to import reverse in tests """
        return reverse(name, args=args, kwargs=kwargs)

    def make_user(self, username='testuser', password='password', perms=None):
        """
        Build a user with <username> and password of 'password' for testing
        purposes.
        """
        if self.user_factory:
            USERNAME_FIELD = getattr(
                self.user_factory._meta.model, 'USERNAME_FIELD', 'username')
            test_user = self.user_factory(**{
                USERNAME_FIELD: username,
            })
            test_user.set_password(password)
            test_user.save()
        else:
            test_user = User.objects.create_user(
                username,
                '{0}@example.com'.format(username),
                password,
            )

        if perms:
            _filter = Q()
            for perm in perms:
                if '.' not in perm:
                    raise ImproperlyConfigured(
                        'The permission in the perms argument needs to be either '
                        'app_label.codename or app_label.* (e.g. accounts.change_user or accounts.*)'
                    )

                app_label, codename = perm.split('.')
                if codename == '*':
                    _filter = _filter | Q(content_type__app_label=app_label)
                else:
                    _filter = _filter | Q(content_type__app_label=app_label, codename=codename)

            test_user.user_permissions.add(*list(Permission.objects.filter(_filter)))

        return test_user

    def assertNumQueriesLessThan(self, num, *args, **kwargs):
        func = kwargs.pop('func', None)
        using = kwargs.pop("using", DEFAULT_DB_ALIAS)
        conn = connections[using]

        context = _AssertNumQueriesLessThanContext(self, num, conn)
        if func is None:
            return context

        with context:
            func(*args, **kwargs)

    def assertGoodView(self, url_name, *args, **kwargs):
        """
        Quick-n-dirty testing of a given url name.
        Ensures URL returns a 200 status and that generates less than 50
        database queries.
        """
        query_count = kwargs.pop('test_query_count', 50)

        with self.assertNumQueriesLessThan(query_count):
            response = self.get(url_name, *args, **kwargs)

        self.response_200(response)

        return response

    def assertInContext(self, key):
        if self.last_response is not None:
            self.assertTrue(key in self.last_response.context)
        else:
            raise NoPreviousResponse("There isn't a previous response to query")

    def get_context(self, key):
        if self.last_response is not None:
            self.assertTrue(key in self.last_response.context)
            return self.last_response.context[key]
        else:
            raise NoPreviousResponse("There isn't a previous response to query")

    def assertContext(self, key, value):
        if self.last_response is not None:
            self.assertEqual(self.last_response.context[key], value)
        else:
            raise NoPreviousResponse("There isn't a previous response to query")


# Note this class inherits from TestCase defined above.
class CBVTestCase(TestCase):
    """
    Directly calls class-based generic view methods,
    bypassing the Django test Client.

    This process bypasses middleware invocation and URL resolvers.

    Example usage:

        from myapp.views import MyClass

        class MyClassTest(CBVTestCase):

            def test_special_method(self):
                request = RequestFactory().get('/')
                instance = self.get_instance(MyClass, request=request)

                # invoke a MyClass method
                result = instance.special_method()

                # make assertions
                self.assertTrue(result)
    """

    def get_instance(self, cls, *args, **kwargs):
        """
        Returns a decorated instance of a class-based generic view class.

        Use `initkwargs` to set expected class attributes.
        For example, set the `object` attribute on MyDetailView class:

            instance = self.get_instance(MyDetailView, initkwargs={'object': obj}, request)

        because SingleObjectMixin (part of generic.DetailView)
        expects self.object to be set before invoking get_context_data().

        `args` and `kwargs` are the same values you would pass to ``reverse()``.
        """
        initkwargs = kwargs.pop('initkwargs', None)
        request = kwargs.pop('request', None)
        if initkwargs is None:
            initkwargs = {}
        instance = cls(**initkwargs)
        instance.request = request
        instance.args = args
        instance.kwargs = kwargs
        return instance

    def get(self, cls, *args, **kwargs):
        """
        Calls cls.get() method after instantiating view class
        with `initkwargs`.
        Renders view templates and sets context if appropriate.
        """
        initkwargs = kwargs.pop('initkwargs', None)
        if initkwargs is None:
            initkwargs = {}
        request = RequestFactory().get('/')
        instance = self.get_instance(cls, initkwargs=initkwargs, request=request, **kwargs)
        self.last_response = self.get_response(request, instance.get)
        self.context = self.last_response.context
        return self.last_response

    def post(self, cls, *args, **kwargs):
        """
        Calls cls.post() method after instantiating view class
        with `initkwargs`.
        Renders view templates and sets context if appropriate.
        """
        data = kwargs.pop('data', None)
        initkwargs = kwargs.pop('initkwargs', None)
        if data is None:
            data = {}
        if initkwargs is None:
            initkwargs = {}
        request = RequestFactory().post('/', data)
        instance = self.get_instance(cls, initkwargs=initkwargs, request=request, **kwargs)
        self.last_response = self.get_response(request, instance.post)
        self.context = self.last_response.context
        return self.last_response

    def get_response(self, request, view_func):
        """
        Obtain response from view class method (typically get or post).

        No middleware is invoked, but templates are rendered
        and context saved if appropriate.
        """
        # Curry a data dictionary into an instance of
        # the template renderer callback function.
        data = {}
        on_template_render = curry(store_rendered_templates, data)
        signal_uid = "template-render-%s" % id(request)
        signals.template_rendered.connect(on_template_render, dispatch_uid=signal_uid)
        try:
            response = view_func(request)

            if hasattr(response, 'render') and callable(response.render):
                response = response.render()
                # Add any rendered template detail to the response.
                response.templates = data.get("templates", [])
                response.context = data.get("context")
            else:
                response.templates = None
                response.context = None

            return response
        finally:
            signals.template_rendered.disconnect(dispatch_uid=signal_uid)

    def get_check_200(self, cls, *args, **kwargs):
        """ Test that we can GET a page and it returns a 200 """
        initkwargs = kwargs.pop('initkwargs', None)
        response = self.get(cls, initkwargs=initkwargs, *args, **kwargs)
        self.response_200(response)
        return response

    def assertGoodView(self, cls, *args, **kwargs):
        """
        Quick-n-dirty testing of a given view.
        Ensures view returns a 200 status and that generates less than 50
        database queries.
        """
        initkwargs = kwargs.pop('initkwargs', None)
        query_count = kwargs.pop('test_query_count', 50)

        with self.assertNumQueriesLessThan(query_count):
            response = self.get(cls, initkwargs=initkwargs, *args, **kwargs)
        self.response_200(response)
        return response
