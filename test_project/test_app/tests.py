import factory
import django
import unittest
import warnings

from distutils.version import LooseVersion

from test_plus.test import TestCase, NoPreviousResponse

DJANGO_16 = LooseVersion(django.get_version()) >= LooseVersion('1.6')

if DJANGO_16:
    from django.contrib.auth import get_user_model
    User = get_user_model()
else:
    from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'user{}'.format(n))
    email = factory.Sequence(lambda n: 'user{}@example.com'.format(n))

    class Meta:
        model = User


class TestPlusUserFactoryOption(TestCase):
    user_factory = UserFactory

    def test_make_user_factory(self):
        u1 = self.make_user('factory')
        self.assertEqual(u1.username, 'factory')


class TestPlusViewTests(TestCase):

    def test_get(self):
        res = self.get('view-200')
        self.assertEqual(res.status_code, 200)

        url = self.reverse('view-200')
        res = self.get(url)
        self.assertEqual(res.status_code, 200)

    def test_get_query(self):
        res = self.get('view-200', data={'query': 'foo'})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.request['QUERY_STRING'], 'query=foo')

    def test_post(self):
        url = self.reverse('view-200')
        data = {'testing': True}
        res = self.post(url, data=data)
        self.assertTrue(res.status_code, 200)

    def test_get_check_200(self):
        res = self.get_check_200('view-200')
        self.assertTrue(res.status_code, 200)

    def test_response_200(self):
        res = self.get('view-200')
        self.response_200(res)

        # Test without response option
        self.response_200()

    def test_response_201(self):
        res = self.get('view-201')
        self.response_201(res)

        # Test without response option
        self.response_201()

    def test_response_302(self):
        res = self.get('view-302')
        self.response_302(res)

        # Test without response option
        self.response_302()

    def test_response_403(self):
        res = self.get('view-403')
        self.response_403(res)

        # Test without response option
        self.response_403()

    def test_response_404(self):
        res = self.get('view-404')
        self.response_404(res)

        # Test without response option
        self.response_404()

    def test_make_user(self):
        """ Test make_user using django.contrib.auth defaults """
        u1 = self.make_user('u1')
        self.assertEqual(u1.username, 'u1')

    def test_login_required(self):
        self.assertLoginRequired('view-needs-login')

        # Make a user and login with our login context
        self.make_user('test')
        with self.login(username='test', password='password'):
            self.get_check_200('view-needs-login')

    def test_login_no_password(self):

        user = self.make_user('test')
        with self.login(username=user.username):
            self.get_check_200('view-needs-login')

    def test_login_user_object(self):

        user = self.make_user('test')
        with self.login(user):
            self.get_check_200('view-needs-login')

    def test_reverse(self):
        self.assertEqual(self.reverse('view-200'), '/view/200/')

    def test_assertgoodview(self):
        self.assertGoodView('view-200')

    def test_assertnumqueries(self):
        with self.assertNumQueriesLessThan(1):
            self.get('view-needs-login')

    def test_assertnumqueries_data_1(self):
        with self.assertNumQueriesLessThan(1):
            self.get('view-data-1')

    def test_assertnumqueries_data_5(self):
        with self.assertNumQueriesLessThan(5):
            self.get('view-data-5')

    @unittest.expectedFailure
    def test_assertnumqueries_failure(self):
        if not DJANGO_16:
            return unittest.skip("Does not work before Django 1.6")

        with self.assertNumQueriesLessThan(1):
            self.get('view-data-5')

    def test_assertnumqueries_warning(self):
        if not DJANGO_16:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")

                with self.assertNumQueriesLessThan(1):
                    self.get('view-data-1')

                self.assertEqual(len(w), 1)
                self.assertTrue('skipped' in str(w[-1].message))
        else:
            return unittest.skip("Only useful for Django 1.6 and before")

    def test_assertincontext(self):
        response = self.get('view-context-with')
        self.assertTrue('testvalue' in response.context)

        self.assertInContext('testvalue')
        self.assertTrue(self.context['testvalue'], response.context['testvalue'])

    def test_get_context(self):
        response = self.get('view-context-with')
        self.assertTrue('testvalue' in response.context)
        value = self.get_context('testvalue')
        self.assertEqual(value, True)

    def test_assert_context(self):
        response = self.get('view-context-with')
        self.assertTrue('testvalue' in response.context)
        self.assertContext('testvalue', True)

    @unittest.expectedFailure
    def test_assertnotincontext(self):
        self.get('view-context-without')
        self.assertInContext('testvalue')

    def test_no_response(self):
        with self.assertRaises(NoPreviousResponse):
            self.assertInContext('testvalue')

    def test_get_is_ajax(self):
        response = self.get('view-is-ajax',
                            extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.response_200(response)

    def test_post_is_ajax(self):
        response = self.post('view-is-ajax',
                             data={'item': 1},
                             extra={'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.response_200(response)
