
# Личный дневник (Diary App)

Простой веб-приложение для ведения личного дневника с возможностью создания, редактирования и удаления записей. Приложение включает в себя систему аутентификации, регистрацию пользователей, а также возможность поиска записей.

## Требования

- Python 3.8+
- Poetry (для управления зависимостями)

## Установка

1. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/AlexanderMalach/sky_pro_final_project.git
   cd diary
   ```

2. Установите зависимости с помощью Poetry:

   ```bash
   poetry install
   ```

3. Активируйте виртуальное окружение:

   ```bash
   poetry shell
   ```

4. Выполните миграции базы данных:

   ```bash
   python manage.py migrate
   ```

5. Запустите сервер разработки:

   ```bash
   python manage.py runserver
   ```

   Приложение будет доступно по адресу `http://127.0.0.1:8000/`.

## Структура проекта

- `diary/`: Основной каталог приложения.
  - `models.py`: Модели данных для записей дневника.
  - `views.py`: Контроллеры для обработки запросов и отображения данных.
  - `urls.py`: Список маршрутов и их обработчиков.
  - `forms.py`: Формы для работы с записями.
  - `templates/`: HTML-шаблоны.
  - `templatetags/my_tags.py`: Статические файлы (CSS, JS и изображения).
- `users/`: Основной каталог приложения.
  - `models.py`: Модели данных для записей дневника.
  - `views.py`: Контроллеры для обработки запросов и отображения данных.
  - `urls.py`: Список маршрутов и их обработчиков.
  - `forms.py`: Формы для работы с записями.
  - `templates/`: HTML-шаблоны.
- `static/`: Статические файлы (CSS, JS и изображения).
- `media/`:  Изображения пользователей.
- `docker-compose.yml/`: .
- `Dockerfile/`: .

## Функциональность

- **Аутентификация пользователей**: Регистрация, вход и выход.
- **Личный дневник**: Добавление, редактирование, удаление записей.
- **Поиск по записям**: Возможность поиска записей по заголовку или содержимому.
- **Управление записями**: Записи доступны только их авторам.

## Технологии

- Django 4.2+
- Bootstrap 5
- PostgreSQL
- JavaScript(AJAX)
- TinyMCE


1. Форкните репозиторий.
2. Создайте новую ветку для ваших изменений (`git checkout -b feature-name`).
3. Сделайте изменения и отправьте их (`git commit -am 'Add new feature'`).
4. Отправьте пулл-реквест.

## Автор

[Aлександр Малахинский](https://github.com/AlexanderMalach)
