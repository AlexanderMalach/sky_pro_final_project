from django.contrib import admin
from .models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """Настройки отображения модели Entry в админке."""

    list_display = ("title", "author", "created_at", "updated_at", "view_counter")
    list_filter = ("author", "created_at", "updated_at")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at", "view_counter")
    fieldsets = (
        (None, {
            "fields": ("title", "content", "image", "author")
        }),
        ("Дополнительная информация", {
            "fields": ("created_at", "updated_at", "view_counter"),
            "classes": ("collapse",)
        }),
    )
