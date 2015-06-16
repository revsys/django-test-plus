import warnings
import django
from django.conf import settings
from django.core.urlresolvers import reverse, resolve, NoReverseMatch
from django.db import connections, DEFAULT_DB_ALIAS
from django.test import TestCase
from distutils.version import LooseVersion


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
                executed <= self.num, "%d queries executed, expected less than %d" % (
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
            credentials.update({
                'username': args[0].username,
                'password': 'password',
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


class TestCase(TestCase):
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
        extra = kwargs.pop("extra", {})
        data = kwargs.pop("data", {})
        try:
            self.last_response = self.client.get(reverse(url_name, args=args, kwargs=kwargs), data=data, **extra)
        except NoReverseMatch:
            self.last_response = self.client.get(url_name, data=data, **extra)

        self.context = self.last_response.context
        return self.last_response

    def post(self, url_name, *args, **kwargs):
        """
        POST to url by name using reverse()

        If reverse raises NoReverseMatch attempt to use it as a URL.
        """
        data = kwargs.pop("data", None)
        extra = kwargs.pop("extra", {})
        try:
            self.last_response = self.client.post(reverse(url_name, args=args, kwargs=kwargs), data, **extra)
        except NoReverseMatch:
            self.last_response = self.client.post(url_name, data, **extra)

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

    def response_403(self, response=None):
        """ Given response has status_code 403 """
        response = self._which_response(response)
        self.assertEqual(response.status_code, 403)

    def response_404(self, response=None):
        """ Given response has status_code 404 """
        response = self._which_response(response)
        self.assertEqual(response.status_code, 404)

    def get_check_200(self, url, *args, **kwargs):
        """ Test that we can GET a page and it returns a 200 """
        response = self.get(url, *args, **kwargs)
        self.response_200(response)
        return response

    def assertLoginRequired(self, url, *args, **kwargs):
        """ Ensure login is required to GET this URL """
        res = self.get(url, *args, **kwargs)
        reversed_url = reverse(url, args=args, kwargs=kwargs)
        expected_url = "{0}?next={1}".format(settings.LOGIN_URL, reversed_url)
        self.assertRedirects(res, expected_url)

    def login(self, *args, **credentials):
        """ Login a user """
        return login(self, *args, **credentials)

    def reverse(self, name, *args, **kwargs):
        """ Reverse a url, convience to avoid having to import reverse in tests """
        return reverse(name, args=args, kwargs=kwargs)

    def make_user(self, username):
        """
        Build a user with <username> and password of 'password' for testing
        purposes.  Exposes the user as self.user_<username>
        """
        if self.user_factory:
            test_user = self.user_factory(username=username)
            test_user.set_password('password')
            test_user.save()
            return test_user
        else:
            test_user = User.objects.create_user(
                username,
                '{0}@example.com'.format(username),
                'password',
            )
            return test_user

    def assertNumQueriesLessThan(self, num, func=None, *args, **kwargs):
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