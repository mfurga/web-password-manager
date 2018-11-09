from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate
from django import forms


class SigninForm(forms.Form):
    """
    Form representation of the user credentials.
    """
    username = forms.CharField(max_length=50, label=_('Username'),
                               widget=forms.TextInput(attrs={'placeholder': _('username')}))
    password = forms.CharField(max_length=50, label=_('Password'),
                               widget=forms.PasswordInput(attrs={'placeholder': _('password')}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError(_('Username or password incorrent.'))
        return super().clean()
