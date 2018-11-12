from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
from django.db import models

from .utils import Crypto


class Entry(models.Model):
    """
    A model represesentation of the single entry that will be stored
    in the database.

    .. py:attribute:: name
       A name that will be used to identify an individual entry.

    .. py:attribute:: url
       URL of the entry.

    .. py:attribute:: login
       Login of the entry.

    .. py:attribute:: password
       An encrypted form of the password with a maximum length of 90 characters.
       NOTE: The real password length is limited to 50 characters.
    """
    name = models.CharField(_('name'), max_length=50)
    url = models.URLField(_('url'), max_length=200)
    login = models.CharField(_('login'), max_length=50)
    password = models.CharField(_('password'), max_length=90)

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')
        ordering = ['name', 'url']

    def __str__(self):
        return f'{self.name} ({self.url})'


def pre_save_encrypt_password(sender, instance, *args, **kwargs):
    instance.password = Crypto().encrypt(instance.password)


pre_save.connect(pre_save_encrypt_password, sender=Entry)
