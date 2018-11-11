from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    """Form representation of the single entry based on `Entry` model."""

    class Meta:
        model = Entry
        fields = ['name', 'url', 'login', 'password']
        labels = {
            'name': _('name'), 'url': _('url'),
            'login': _('login'), 'password': _('password')
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('name')}),
            'url': forms.URLInput(attrs={'placeholder': _('url')}),
            'login': forms.TextInput(attrs={'placeholder': _('login')}),
            'password': forms.PasswordInput(attrs={'placeholder': _('password')})
        }
