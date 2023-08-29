from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView, View)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
import hashlib
import time

from .models import Entry
from .forms import EntryForm


class EntryListView(LoginRequiredMixin, ListView):
    """
    The entries list view. This view is used to display all entries
    from the database.
    """
    model = Entry
    context_object_name = 'entries'
    template_name = 'entries/entries_list.html'
    paginate_by = 10

    def get_queryset(self):
        try:
            query_name = self.request.GET.get('q')
            queryset = Entry.objects.filter(name__contains=query_name)
        except ValueError:
            queryset = Entry.objects.all()
        return queryset


class EntryDetailView(LoginRequiredMixin, DetailView):
    """
    The entry detail view. This view is used to display detailed informations
    about a specific entry in the database.
    """
    queryset = Entry.objects.all()
    context_object_name = 'entry'
    template_name = 'entries/entries_detail.html'


class EntryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    The entry create view. This view is used to create a new entry in
    the database.
    """
    form_class = EntryForm
    template_name = 'entries/entries_create.html'
    success_url = reverse_lazy('entries:list')
    success_message = _('Entry successfully created.')


class EntryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    The entry update view. This view is used to update existing entries
    in the database.
    """
    model = Entry
    form_class = EntryForm
    template_name = 'entries/entries_update.html'
    success_message = _('Entry successfully updated. (%(name)s)')

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data, name=self.object.name
        )

    def get_success_url(self):
        return reverse('entries:detail', args=[self.object.pk])


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    """
    The entry delete view. This view is used to delete a specific
    entry from the database and redirect the user to the home page.
    """
    model = Entry
    template_name = 'entries/entries_delete.html'
    context_object_name = 'entry'
    success_url = reverse_lazy('entries:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Entry successfully deleted.'))
        return super().delete(request, *args, **kwargs)


class EntryShareView(LoginRequiredMixin, View):
    """
    The entry share view. This view is used to create a URL that allows
    access to a specific entry.

    URL FORMAT:
        http://exmaple.com/entry/share/<hash>/<time>/<pk>/
    WHERE:
        * hash - MD5 hash of (`SHARE_SECRET_SALT` + expiration time + pk).
        * time - time of entry expiry (UNIX timestamp in seconds).
        * pk - primary key of the entry.
    """

    def get(self, request, *args, **kwargs):
        SHARE_SECRET_SALT = settings.SHARE_SECRET_SALT

        expiration_time = int(time.time()) + 5 * 60
        to_hash = '{salt}{time}{pk}'.format(salt=SHARE_SECRET_SALT,
                                            time=expiration_time,
                                            pk=kwargs['pk'])
        link_hash = hashlib.md5(to_hash.encode('utf-8')).hexdigest()

        link = reverse('entries:share-check',
                       kwargs={'hash': link_hash, 'time': expiration_time, 'pk': kwargs['pk']})
        link = request.build_absolute_uri(link)
        return render(request, 'entries/entries_share.html', {'link': link})


class EntryShareCheckView(View):
    """
    The entry share check view. This view is used to validate a shared
    URL and gives permission to a specific entry.
    """

    def get(self, request, *args, **kwargs):
        SHARE_SECRET_SALT = settings.SHARE_SECRET_SALT

        url_hash, url_time, url_pk = kwargs['hash'], kwargs['time'], kwargs['pk']
        to_hash = '{salt}{time}{pk}'.format(salt=SHARE_SECRET_SALT,
                                            time=url_time,
                                            pk=url_pk)
        link_hash = hashlib.md5(to_hash.encode('utf-8')).hexdigest()

        if link_hash != url_hash or (int(time.time()) - url_time) > 0:
            raise Http404

        entry = Entry.objects.get(pk=kwargs['pk'])
        return render(request, 'entries/entries_detail.html', {'entry': entry})
