from django.contrib.auth.forms import UserCreationForm
from django.forms import Form, EmailField

from diary.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class PasswordResetForm(Form):
    email = EmailField(label="Email", max_length=254)
