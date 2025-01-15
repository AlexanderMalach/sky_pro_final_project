from django.db import models
from django.conf import settings
from django.urls import reverse

from users.models import User


class Entry(models.Model):
    """Модель для записей в личном дневнике."""

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержимое")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    image = models.ImageField(verbose_name="Картинка", blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор", related_name="entries"
    )
    view_counter = models.PositiveIntegerField(verbose_name="Cчётчик просмотров", default=0)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает URL для просмотра детальной информации о записи."""
        return reverse("entry_detail", args=[str(self.id)])
