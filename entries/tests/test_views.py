from django.utils.translation import ugettext as _
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from entries.utils import Crypto
from entries.models import Entry


class EntryListViewTest(TestCase):
    """The tests for the entry list view."""

    def setUp(self):
        self.user = User.objects.create_user(username='rik', password='pass')
        self.client = Client()

    def test_not_logged_user_entry_list(self):
        response = self.client.get(reverse('entries:list'), {})
        self.assertRedirects(response, '/account/signin/?next=/',
                             target_status_code=200)

    def test_logged_user_entry_list(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(reverse('entries:list'), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entries_list.html')
        self.assertEqual(len(response.context['entries']), 0)

    def test_logged_user_entry_list_search(self):
        self.client.force_login(self.user, backend=None)
        searching_text = 'facebook'
        response = self.client.get(reverse('entries:list'), {'q': searching_text})
        self.assertContains(response, searching_text, status_code=200)


class EntryDetailViewTest(TestCase):
    """The tests for the entry detail view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='rik', password='pass')
        self.entry = Entry.objects.create(name='facebook', url='https://facebook.com',
                                          login='rik', password='password')

    def test_not_logged_user_entry_detail(self):
        response = self.client.get(reverse('entries:detail', args=[self.entry.id]))
        self.assertRedirects(response,
                             f'/account/signin/?next={reverse("entries:detail", args=[self.entry.id])}',
                             target_status_code=200)

    def test_logged_user_entry_detail(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(reverse('entries:detail', args=[self.entry.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entries_detail.html')
        self.assertEqual(response.context['entry'].name, self.entry.name)


class EntryCreateViewTest(TestCase):
    """The tests for the entry create view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='rik', password='pass')

    def test_not_logged_user_entry_create(self):
        response = self.client.get(reverse('entries:create'))
        self.assertRedirects(response, f'/account/signin/?next={reverse("entries:create")}',
                             target_status_code=200)

    def test_logged_user_entry_create(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(reverse('entries:create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entries_create.html')

    def test_logged_user_entry_create_post(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.post(reverse('entries:create'), {
            'name': 'facebook', 'url': 'https://facebook.com',
            'login': 'user', 'password': 'password'
        })
        messages = [m.message for m in get_messages(response.wsgi_request)]

        self.assertRedirects(response, reverse('entries:list'), target_status_code=200)
        self.assertIn(_('Entry successfully created.'), messages)
        self.assertEqual(Entry.objects.first().name, 'facebook')
        self.assertEqual(Entry.objects.first().url, 'https://facebook.com')
        self.assertEqual(Entry.objects.first().login, 'user')
        self.assertEqual(Entry.objects.first().password, Crypto().encrypt('password'))


class EntryUpdateViewTest(TestCase):
    """The tests for the entry update view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='rik', password='pass')
        self.entry = Entry.objects.create(name='facebook', url='https://facebook.com',
                                          login='user', password='password')

    def test_not_logged_user_entry_update(self):
        response = self.client.get(reverse('entries:update', args=[self.entry.id]))
        self.assertRedirects(response,
                             f'/account/signin/?next={reverse("entries:update", args=[self.entry.id])}',
                             target_status_code=200)

    def test_logged_user_entry_update(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(reverse('entries:update', args=[self.entry.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entries_update.html')
        self.assertEqual(response.context['entry'].name, self.entry.name)

    def test_logged_user_entry_update_post(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.post(reverse('entries:update', args=[self.entry.id]), {
            'name': 'google', 'url': 'https://google.com', 'login': 'rik', 'password': 'password'
        })

        self.assertRedirects(response, reverse('entries:detail', args=[self.entry.id]),
                             target_status_code=200)
        self.assertEqual(Entry.objects.first().name, 'google')
        self.assertEqual(Entry.objects.first().url, 'https://google.com')
        self.assertEqual(Entry.objects.first().login, 'rik')


class EntryDeleteViewTest(TestCase):
    """The tests for the entry delete view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='rik', password='pass')
        self.entry = Entry.objects.create(name='facebook', url='https://facebook.com',
                                          login='rik', password='password')

    def test_not_logged_user_entry_delete(self):
        response = self.client.get(reverse('entries:delete', args=[self.entry.id]))
        self.assertRedirects(response, f'/account/signin/?next={reverse("entries:delete", args=[self.entry.id])}',
                             target_status_code=200)

    def test_logged_user_entry_delete(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.get(reverse('entries:delete', args=[self.entry.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entries/entries_delete.html')
        self.assertEqual(response.context['entry'].name, self.entry.name)

    def test_logged_user_entry_delete_post(self):
        self.client.force_login(self.user, backend=None)
        response = self.client.post(reverse('entries:delete', args=[self.entry.id]), {})
        messages = [m.message for m in get_messages(response.wsgi_request)]

        with self.assertRaises(Entry.DoesNotExist):
            Entry.objects.get(id=self.entry.id)
        self.assertRedirects(response, reverse('entries:list'), target_status_code=200)
        self.assertIn(_('Entry successfully deleted.'), messages)
