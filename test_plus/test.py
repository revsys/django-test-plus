import django
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import connections, DEFAULT_DB_ALIAS
from django.test import TestCase
from distutils.version import LooseVersion

if LooseVersion(django.get_version()) >= LooseVersion('1.6'):
    from django.test.utils import CaptureQueriesContext
    CAPTURE = True
else:
    CAPTURE = False


class login(object):
    def __init__(self, testcase, **credentials):
        self.testcase = testcase
        success = testcase.client.login(**credentials)
        self.testcase.assertTrue(
            success,
            "login failed with credentials=%r" % (credentials)
        )

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.testcase.client.logout()


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


class TestCase(TestCase):
    """
    Django TestCase with helpful additional features
    """
    user_factory = None

    def tearDown(self):
        self.client.logout()

    def get(self, url_name, *args, **kwargs):
        """ GET url by name using reverse() """
        return self.client.get(reverse(url_name, args=args, kwargs=kwargs))

    def post(self, url_name, *args, **kwargs):
        """ POST to url by name using reverse() """
        data = kwargs.pop("data", None)
        return self.client.post(reverse(url_name, args=args, kwargs=kwargs), data)

    def response_200(self, response):
        """ Given response has status_code 200 """
        self.assertEqual(response.status_code, 200)

    def response_201(self, response):
        """ Given response has status_code 201 """
        self.assertEqual(response.status_code, 201)

    def response_302(self, response):
        """ Given response has status_code 302 """
        self.assertEqual(response.status_code, 302)

    def response_403(self, response):
        """ Given response has status_code 403 """
        self.assertEqual(response.status_code, 403)

    def response_404(self, response):
        """ Given response has status_code 404 """
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

    def login(self, **credentials):
        """ Login a user """
        return login(self, **credentials)

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
            if LooseVersion(django.get_version()) >= LooseVersion('1.6'):
                from django.contrib.auth import get_user_model
                User = get_user_model()
            else:
                from django.contrib.auth.models import User

            test_user = User.objects.create_user(
                username,
                '{0}@example.com'.format(username),
                'password',
            )
            return test_user

    def assertNumQueriesLessThan(self, num, func=None, *args, **kwargs):
        if CAPTURE:
            using = kwargs.pop("using", DEFAULT_DB_ALIAS)
            conn = connections[using]

            context = _AssertNumQueriesLessThanContext(self, num, conn)
            if func is None:
                return context

            with context:
                func(*args, **kwargs)
        else:
            func(*args, **kwargs)

    def assertGoodView(self, url_name, *args, **kwargs):
        """
        Quick-n-dirty testing of a given url name.
        Ensures URL returns a 200 status and that generates less than 100
        database queries.
        """
        query_count = kwargs.pop('test_query_count', 100)

        with self.assertNumQueriesLessThan(query_count):
            response = self.get(url_name, *args, **kwargs)

        self.response_200(response)

