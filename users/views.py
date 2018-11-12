from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, RedirectView
from django.utils.translation import ugettext as _
from django.urls import reverse_lazy
from django.contrib import messages

from users.forms import SigninForm


class ForNotLoggedOnly(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated


class SinginView(ForNotLoggedOnly, FormView):
    """
    The users sign in view. This view provides login authorization
    for users.
    """
    template_name = 'users/users_signin.html'
    form_class = SigninForm

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        login(self.request, user)
        messages.success(self.request, _('Successfully logged in.'))
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('entries:list'))


class LogoutView(LoginRequiredMixin, RedirectView):
    """
    The users logout view. This view allows to log out of the account.
    """
    url = reverse_lazy('users:signin')
    login_url = reverse_lazy('users:signin')

    def get(self, request, *args, **kwargs):
        messages.success(request, _('Successfully logged out.'))
        logout(request)
        return super().get(request, *args, **kwargs)
