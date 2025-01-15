from django.urls import path

from diary.apps import DiaryConfig
from diary.views import (
    EntryListView,
    EntryDetailView,
    EntryCreateView,
    EntryDeleteView,
    EntryUpdateView,
)

app_name = DiaryConfig.name

urlpatterns = [
    path("", EntryListView.as_view(), name="entry_list"),
    path("entry/<int:pk>/", EntryDetailView.as_view(), name="entry_detail"),
    path("entry/create/", EntryCreateView.as_view(), name="entry_create"),
    path("entry/<int:pk>/update/", EntryUpdateView.as_view(), name="entry_update"),
    path("entry/<int:pk>/delete/", EntryDeleteView.as_view(), name="entry_delete"),
]
