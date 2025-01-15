import secrets

from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        send_mail(
            subject="Confirm your email",
            message=f"Hi! Click the link to confirm your email: {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


def reset_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                user = User.objects.get(email=email)
                new_password = get_random_string(length=8)
                user.set_password(new_password)
                user.save()
                send_mail(
                    "Ваш новый пароль",
                    f"Ваш новый пароль: {new_password}",
                    "EMAIL_HOST_USER",
                    [email],
                    fail_silently=False,
                )
                messages.success(
                    request, "Новый пароль отправлен на вашу электронную почту."
                )
                return redirect(reverse("users:login"))
            except User.DoesNotExist:
                messages.error(
                    request, "Пользователь с таким адресом электронной почты не найден."
                )
    else:
        form = PasswordResetForm()
    return render(request, "users/reset_password.html", {"form": form})
