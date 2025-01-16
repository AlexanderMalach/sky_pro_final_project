from django.test import TestCase
from django.urls import reverse
from django.test import TestCase
from diary.models import Entry
from users.models import User


class EntryViewTests(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(email="testuser@example.com")
        self.user.set_password("password")
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.is_active = True
        self.user.save()
        # Создаем запись для тестов
        self.entry = Entry.objects.create(
            title="Test Entry",
            content="Test Content",
            author=self.user
        )

    def test_entry_list_view(self):
        # Проверяем, что страница для списка записей доступна
        self.client.login(email="testuser@example.com", password="password")
        response = self.client.get(reverse('diary:entry_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Entry")  # Проверка наличия записи в списке

    def test_entry_detail_view(self):
        # Проверяем, что страница детали записи доступна
        self.client.login(email="testuser@example.com", password="password")
        response = self.client.get(reverse('diary:entry_detail', args=[self.entry.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Entry")
    #
    def test_entry_create_view(self):
        # Проверяем создание записи
        self.client.login(email="testuser@example.com", password="password")
        response = self.client.post(reverse('diary:entry_create'), {
            'title': 'New Entry',
            'content': 'New Content',
            'author': self.user.id,
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление на список записей
        self.assertTrue(Entry.objects.filter(title="New Entry").exists())  # Проверка сохранения записи

    def test_entry_update_view(self):
        # Проверяем обновление записи
        self.client.login(email="testuser@example.com", password="password")
        response = self.client.post(reverse('diary:entry_update', args=[self.entry.id]), {
            'title': 'Updated Test Entry',
            'content': 'Updated Test Content',
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление на страницу детали записи
        self.entry.refresh_from_db()
        self.assertEqual(self.entry.title, "Updated Test Entry")  # Проверка обновления записи

    def test_entry_delete_view(self):
        # Проверяем удаление записи
        self.client.login(email="testuser@example.com", password="password")
        response = self.client.post(reverse('diary:entry_delete', args=[self.entry.id]))
        self.assertEqual(response.status_code, 302)  # Перенаправление на список записей
        self.assertFalse(Entry.objects.filter(id=self.entry.id).exists())  # Проверка удаления записи

    def test_entry_list_view_not_authenticated(self):
        # Проверяем, что неаутентифицированный пользователь не может просматривать записи
        response = self.client.get(reverse('diary:entry_list'))
        self.assertEqual(response.status_code, 302)  # Перенаправление на страницу логина

    def test_entry_create_view_not_authenticated(self):
        # Проверяем, что неаутентифицированный пользователь не может создавать записи
        response = self.client.post(reverse('diary:entry_create'), {
            'title': 'New Entry',
            'content': 'New Content',
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление на страницу логина
