from django.db import models
from django.utils.translation import ugettext_lazy as _


class Entry(models.Model):
    """
    Model represesentation of the single entry.
    """
    name = models.CharField(_('name'), max_length=50)
    url = models.URLField(_('url'), max_length=200)
    login = models.CharField(_('login'), max_length=50)
    password = models.CharField(_('password'), max_length=90)

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = ('entries')
        ordering = ['name']

    def __unicode__(self):
        return f'{self.name} ({self.url})'
