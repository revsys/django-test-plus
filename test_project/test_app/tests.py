from test_plus.test import TestCase


class TestPlusViewTests(TestCase):

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

