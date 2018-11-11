from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.urls import reverse, reverse_lazy
from django.contrib import messages

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
