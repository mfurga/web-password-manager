from django.test import TestCase

from entries.models import Entry


class EntryModelTest(TestCase):
    """The test for the entry model."""

    def setUp(self):
        self.initial_data = {'name': 'facebook', 'url': 'https://facebook.com',
                             'login': 'user', 'password': 'password'}

    def test_string_representation(self):
        entry = Entry(**self.initial_data)
        self.assertEqual(str(entry), '{0[name]} ({0[url]})'.format(self.initial_data))

    def test_verbose_name_plural(self):
        self.assertEqual(str(Entry._meta.verbose_name_plural), 'entries')

    def test_pre_save_password_encryption(self):
        entry = Entry(**self.initial_data)
        self.assertEqual(entry.password, 'password')
        entry.save()
        self.assertEqual(entry.password, 'EgBSBcfow6xrX4xB47i+PQ==')

    def test_entries_ordering(self):
        Entry.objects.create(**self.initial_data)
        self.initial_data['name'] = 'amazon'
        self.initial_data['url'] = 'https://amazon.com'
        Entry.objects.create(**self.initial_data)

        self.assertEqual(Entry.objects.first().name, 'amazon')
