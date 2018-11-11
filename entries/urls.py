from django.urls import path

from .views import (EntryListView, EntryDetailView,
                    EntryCreateView, EntryUpdateView, EntryDeleteView)

app_name = 'entries'
urlpatterns = [
    path('', EntryListView.as_view(), name='list'),
    path('entry/create/', EntryCreateView.as_view(), name='create'),
    path('entry/<int:pk>/', EntryDetailView.as_view(), name='detail'),
    path('entry/<int:pk>/update/', EntryUpdateView.as_view(), name='update'),
    path('entry/<int:pk>/delete/', EntryDeleteView.as_view(), name='delete')
]
