from test_plus.test import TestCase

from .models import Data


class TestPlusViewTests(TestCase):

    def _make_data_rows(self, num=5):
        items = []
        for i in range(num):
            items.append(Data.objects.create(name='data-{}'.format(i)))

        return items

    def test_get(self):
        res = self.get('view-200')
        self.assertTrue(res.status_code, 200)

    def test_get_check_200(self):
        res = self.get_check_200('view-200')
        self.assertTrue(res.status_code, 200)

    def test_response_200(self):
        res = self.get('view-200')
        self.response_200(res)

    def test_response_201(self):
        res = self.get('view-201')
        self.response_201(res)

    def test_response_302(self):
        res = self.get('view-302')
        self.response_302(res)

    def test_response_404(self):
        res = self.get('view-404')
        self.response_404(res)

    def test_login_required(self):
        self.assertLoginRequired('view-needs-login')

        # Make a user and login with our login context
        self.make_user('test')
        with self.login(username='test', password='password'):
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