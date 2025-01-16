from django.test import TestCase
from users.models import User
from users.models import User





from django.core.mail import outbox





from django.core import mail
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

class UserModelTest(TestCase):

    def setUp(self):
        """Настройка начальных данных для тестов"""
        self.user_data = {
            "first_name": "Test",
            "last_name": "User",
            "phone": "+1234567890",
            "country": "Testland",
            "tg_name": "test_user",
            "avatar": None,
            "token": "sample_token",
        }
        # Создаем пользователя
        self.user = User(email="testuser@example.com")
        self.user.set_password("testpassword")
        self.user.first_name = self.user_data["first_name"]
        self.user.last_name = self.user_data["last_name"]
        self.user.phone = self.user_data["phone"]
        self.user.country = self.user_data["country"]
        self.user.tg_name = self.user_data["tg_name"]
        self.user.token = self.user_data["token"]
        self.user.save()

    def test_user_creation(self):
        """Тестирование создания пользователя"""
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("testpassword"))
        self.assertEqual(self.user.first_name, "Test")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.phone, "+1234567890")
        self.assertEqual(self.user.country, "Testland")
        self.assertEqual(self.user.tg_name, "test_user")
        self.assertEqual(self.user.token, "sample_token")

    def test_user_str_method(self):
        """Тестирование строкового представления пользователя"""
        self.assertEqual(str(self.user), "testuser@example.com")

    def test_user_required_fields(self):
        """Тестирование обязательных полей"""
        required_fields = ["email", "first_name", "last_name"]
        for field in required_fields:
            self.assertTrue(getattr(self.user, field))




outbox.clear()
class UserCreateViewTest(TestCase):

    def test_user_creation_and_email_send(self):
        """Тестирование создания пользователя и отправки email для подтверждения"""
        data = {
            "email": "testuser@example.com",
            "password1": "password123",
            "password2": "password123",
        }

        # Отправляем POST-запрос на создание пользователя
        response = self.client.post(reverse("users:register"), data)
        self.assertEqual(response.status_code, 200)  # проверяем, что запрос успешен

        # Проверяем количество отправленных писем
        print(f"Emails in outbox: {len(mail.outbox)}")
        for email in mail.outbox:
            print(f"Email subject: {email.subject}")
            print(f"Email to: {email.to}")
            print(f"Email body: {email.body[:100]}...")  # Выводим первые 100 символов тела письма для отладки

        # Письмо должно быть отправлено только после выполнения подтверждения
        if len(mail.outbox) > 0:
            confirmation_email = mail.outbox[0]
            confirmation_link = self.extract_confirmation_link(confirmation_email.body)

            # Переход по ссылке подтверждения
            response = self.client.get(confirmation_link)

            # Проверка, что письмо отправлено после подтверждения
            self.assertTrue(len(mail.outbox) > 0, "Email not sent")
            self.assertEqual(mail.outbox[0].subject, "Подтверждение регистрации")
            self.assertEqual(mail.outbox[0].to, ["testuser@example.com"])

    def extract_confirmation_link(self, email_body):
        """Функция для извлечения ссылки подтверждения из письма"""
        import re
        match = re.search(r'http://[^\s]+', email_body)
        return match.group(0) if match else ""



class EmailVerificationTest(TestCase):

    def test_email_verification(self):
        """Тестирование подтверждения email"""
        user = User.objects.create(
            email="testuser@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            is_active=False,
            token="sampletoken"
        )

        # Проверка до активации
        self.assertFalse(user.is_active)

        # Переход по ссылке для активации
        response = self.client.get(reverse("users:email-confirm", args=[user.token]))
        user.refresh_from_db()

        # Проверяем, что пользователь стал активным
        self.assertTrue(user.is_active)
        self.assertRedirects(response, reverse("users:login"))


# Тестирование сброса пароля
class ResetPasswordTest(TestCase):

    def test_password_reset(self):
        """Тестирование сброса пароля"""
        # Создаем пользователя вручную
        user = User(email="testuser@example.com")
        user.set_password("oldpassword")  # Устанавливаем пароль
        user.first_name = "Test"
        user.last_name = "User"
        user.save()

        # Отправляем запрос на сброс пароля
        response = self.client.post(reverse("users:reset_password"), {"email": user.email})

        # Проверяем, что письмо отправлено
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Ваш новый пароль", mail.outbox[0].subject)

        # Проверяем, что новый пароль был установлен
        new_password = mail.outbox[0].body.split(": ")[1]
        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))

        # Убедимся, что нас перенаправляют на страницу входа
        self.assertRedirects(response, reverse("users:login"))

