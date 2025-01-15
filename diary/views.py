from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from diary.forms import EntryForm
from diary.models import Entry


class EntryListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = "diary/entry_list.html"  # Укажите путь к вашему шаблону

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Entry.objects.filter(author=self.request.user)
        else:
            queryset = Entry.objects.none()  # Пустой запрос для анонимных пользователей

        query = self.request.GET.get("q", "")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )

        return queryset


class EntryDetailView(LoginRequiredMixin, DetailView):
    model = Entry

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_counter += 1
        self.object.save()
        return self.object

    def get_queryset(self):
        # Ограничиваем доступ к записи только её автору
        return Entry.objects.filter(author=self.request.user)


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy("diary:entry_list")

    def form_valid(self, form):
        # Сохраняем объект, но не записываем в базу
        entry = form.save(commit=False)
        # Присваиваем текущего пользователя как автора
        entry.author = self.request.user
        # Сохраняем объект в базу
        entry.save()
        return super().form_valid(form)


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    success_url = reverse_lazy("diary:entry_list")

    def get_success_url(self):
        return reverse_lazy("diary:entry_detail", args=[self.kwargs.get("pk")])

    def get_queryset(self):
        # Ограничиваем редактирование только для автора записи
        return Entry.objects.filter(author=self.request.user)


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    success_url = reverse_lazy("diary:entry_list")

    def get_queryset(self):
        # Ограничиваем удаление только для автора записи
        return Entry.objects.filter(author=self.request.user)
