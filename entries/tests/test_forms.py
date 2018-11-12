from django.utils.translation import gettext_lazy as _
from django.test import TestCase

from entries.forms import EntryForm


class EntryFormTest(TestCase):
    """The test for the entry form."""

    def setUp(self):
        self.initial_data = {'name': 'facebook', 'url': 'https://facebook.com',
                             'login': 'user', 'password': 'password'}

    def test_valid_initial_data(self):
        form = EntryForm(data=self.initial_data)
        self.assertTrue(form.is_valid())

    def test_password_max_length(self):
        self.initial_data['password'] = 'x' * 51
        form = EntryForm(data=self.initial_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password'],
            [
                _('The password is too long. (max 50 characters)')
            ]
        )

    def test_name_max_length(self):
        self.initial_data['name'] = 'x' * 51
        form = EntryForm(data=self.initial_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['name'],
            [
                _('Ensure this value has at most 50 characters (it has 51).')
            ]
        )

    def test_url_max_length(self):
        self.initial_data['url'] = 'http://google.com/' + 'x' * 200
        form = EntryForm(data=self.initial_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['url'],
            [
                _('Ensure this value has at most 200 characters (it has 218).')
            ]
        )

    def test_invalid_url(self):
        self.initial_data['url'] = 'asdf'
        form = EntryForm(data=self.initial_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['url'],
            [
                _('Enter a valid URL.')
            ]
        )

    def test_login_max_length(self):
        self.initial_data['login'] = 'x' * 51
        form = EntryForm(data=self.initial_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['login'],
            [
                _('Ensure this value has at most 50 characters (it has 51).')
            ]
        )
