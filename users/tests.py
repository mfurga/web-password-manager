from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.test import TestCase, Client


class SigninViewTest(TestCase):
    """The tests for the sign in view."""

    def setUp(self):
        self.user = User.objects.create_user(username='rik', password='pass')
        self.client = Client()

    def test_not_logged_users_signin(self):
        response = self.client.get('/account/signin/', {})
        self.assertEqual(response.status_code, 200)

    def test_logged_user_signin(self):
        self.client.force_login(self.user, backend=None)
        respone = self.client.get('/account/signin/', {})
        self.assertEqual(respone.status_code, 403)

    def test_not_logged_user_invalid_credentials(self):
        response = self.client.post('/account/signin/', {
            'username': 'rik', 'password': 'password'
        })
        self.assertContains(response, _('Username or password incorrent.'))

    def test_not_logged_user_valid_credentials(self):
        respone = self.client.post('/account/signin/', {
            'username': 'rik', 'password': 'pass'
        })
        self.assertRedirects(respone, '/', target_status_code=200)

    def tearDown(self):
        self.user = None


class LogoutViewTest(TestCase):
    """The tests for the logout view."""

    def setUp(self):
        self.user = User.objects.create_user(username='rik', password='pass')
        self.client = Client()

    def test_not_logged_user_logout(self):
        respone = self.client.get('/account/logout/', {})
        self.assertRedirects(respone, '/account/signin/?next=/account/logout/',
                             target_status_code=200)

    def test_logged_user_logout(self):
        self.client.force_login(self.user, backend=None)
        respone = self.client.get('/account/logout/', {})
        self.assertRedirects(respone, '/account/signin/', target_status_code=200)

    def tearDown(self):
        self.user = None
