from django.contrib.auth.models import User
from django.test import TestCase, Client


class EntryListViewTest(TestCase):
    """The tests for the entry list view."""

    def setUp(self):
        self.user = User.objects.create_user(username='rik', password='pass')
        self.client = Client()

    def test_not_logged_user_entry_list(self):
        response = self.client.get('/', {})
        self.assertRedirects(response, '/account/signin/?next=/',
                             target_status_code=200)

    def test_logged_user_entry_list(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get('/', {})
        self.assertContains(response, 'List of entries', status_code=200)

    def tearDown(self):
        self.client = None
        self.user = None
