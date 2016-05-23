import factory
import django
import unittest
import warnings

from distutils.version import LooseVersion

from test_plus.test import (
    CBVTestCase,
    NoPreviousResponse,
    TestCase
)

from .views import (
    CBView,
    CBTemplateView,
)

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

    def test_get_follow(self):
        # Expect 302 status code
        res = self.get('view-redirect')
        self.assertEqual(res.status_code, 302)
        # Expect 200 status code
        url = self.reverse('view-redirect')
        res = self.get(url, follow=True)
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

    def test_post_follow(self):
        url = self.reverse('view-redirect')
        data = {'testing': True}
        # Expect 302 status code
        res = self.post(url, data=data)
        self.assertTrue(res.status_code, 302)
        # Expect 200 status code
        res = self.post(url, data=data, follow=True)
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

    def test_response_401(self):
        res = self.get('view-401')
        self.response_401(res)

        # Test without response option
        self.response_401()

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

    def test_response_405(self):
        res = self.get('view-405')
        self.response_405(res)

        # Test without response option
        self.response_405()

    def test_response_410(self):
        res = self.get('view-410')
        self.response_410(res)

        # Test without response option
        self.response_410()

    def test_make_user(self):
        """ Test make_user using django.contrib.auth defaults """
        u1 = self.make_user('u1')
        self.assertEqual(u1.username, 'u1')

    def test_make_user_with_perms(self):
        u1 = self.make_user('u1', perms=['auth.*'])
        expected_perms = [u'add_group', u'change_group', u'delete_group',
                          u'add_permission', u'change_permission', u'delete_permission',
                          u'add_user', u'change_user', u'delete_user']
        self.assertEqual(list(u1.user_permissions.values_list('codename', flat=True)), expected_perms)

        u2 = self.make_user('u2', perms=['auth.add_group'])
        self.assertEqual(list(u2.user_permissions.values_list('codename', flat=True)), [u'add_group'])

    def test_login_required(self):
        self.assertLoginRequired('view-needs-login')

        # Make a user and login with our login context
        self.make_user('test')
        with self.login(username='test', password='password'):
            self.get_check_200('view-needs-login')

    def test_login_other_password(self):
        # Make a user with a different password
        user = self.make_user('test', password='revsys')
        with self.login(user, password='revsys'):
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
        with self.assertNumQueriesLessThan(2):
            self.get('view-data-1')

    def test_assertnumqueries_data_5(self):
        with self.assertNumQueriesLessThan(6):
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


class TestPlusCBViewTests(CBVTestCase):

    def test_get(self):
        response = self.get(CBView)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        data = {'testing': True}
        response = self.post(CBView, data=data)
        self.assertEqual(response.status_code, 200)

    def test_get_check_200(self):
        self.get_check_200(CBView)

    def test_assert_good_view(self):
        self.assertGoodView(CBView)


class TestPlusCBTemplateViewTests(CBVTestCase):

    def test_get(self):
        response = self.get(CBTemplateView)
        self.assertEqual(response.status_code, 200)
        self.assertInContext('revsys')
        self.assertContext('revsys', 42)
        self.assertTemplateUsed(response, template_name='test.html')

    def test_get_new_template(self):
        template_name = 'other.html'
        response = self.get(CBTemplateView, initkwargs={'template_name': template_name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name=template_name)


class TestPlusCBCustomMethodTests(CBVTestCase):

    def test_custom_method_with_value(self):
        special_value = 42
        instance = self.get_instance(CBView, initkwargs={'special_value': special_value})
        self.assertEqual(instance.special(), special_value)

    def test_custom_method_no_value(self):
        instance = self.get_instance(CBView)
        self.assertFalse(instance.special())
