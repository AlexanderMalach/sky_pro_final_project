from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Настройки отображения кастомной модели User в админке."""

    model = User
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "country")
    search_fields = ("email", "first_name", "last_name", "phone", "tg_name")
    ordering = ("email",)
    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (None, {
            "fields": ("email", "password")
        }),
        ("Личная информация", {
            "fields": ("first_name", "last_name", "phone", "country", "tg_name", "avatar")
        }),
        ("Статус", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        ("Важные даты", {
            "fields": ("last_login", "date_joined"),
        }),
        ("Дополнительно", {
            "fields": ("token",),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_active", "is_staff"),
        }),
    )
