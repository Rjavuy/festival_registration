# Система регистрации участников фестиваля

## Назначение

Приложение для автоматизации подачи и обработки заявок на участие
в фестивалях. Участники регистрируются и подают заявки, организаторы
проверяют их и присваивают статус. Консольная версия (ПР2–ПР3) дополнена
веб-интерфейсом на Django (ПР5), страницы которого
формируются шаблонами Django (ПР6).

## Используемые технологии

- Python 3;
- Django 5.2 – веб-фреймворк;
- Django Template Language (DTL) – шаблоны страниц;
- HTML5, CSS3 и Bootstrap 5.3 – разметка и оформление страниц;
- JavaScript – небольшое клиентское поведение интерфейса;
- pytest – автоматизированные тесты;
- flake8 – проверка качества кода.

## Целевая аудитория

- Участники фестиваля (артисты, волонтёры, гости).
- Организаторы и администраторы фестиваля.

## Предметная область

Организация и проведение массовых мероприятий (фестивалей).
Основные объекты: фестиваль, участник, заявка.

Правила подачи заявки:

- участнику должно быть не меньше 14 лет;
- заявку можно подать не позже даты проведения фестиваля;
- на фестивале должны быть свободные места (их занимают активные заявки –
  со статусами «Отправлена» и «Одобрена»);
- участник не может подать две активные заявки на один фестиваль;
- отменённая или отклонённая заявка не занимает место.

## Возможности

- просмотр фестивалей со свободными местами (сортировка по дате);
- поиск фестиваля по названию;
- отбор предстоящих фестивалей;
- добавление фестиваля;
- регистрация участника с проверкой email, телефона и даты рождения;
- поиск участника по имени или email;
- подача заявки с проверкой возможности участия;
- одобрение и отклонение заявки организатором;
- отмена заявки (заявка остаётся в списке со статусом «Отменена»);
- статистика заявок по статусам;
- сохранение данных в JSON между запусками.

## Основные классы

### Festival – фестиваль (`models/festivals.py`)

Атрибуты: `id`, `name`, `festival_date`, `max_places`.

Методы:

- `is_registration_open(current_date)` – принимаются ли заявки на дату;
- `has_free_places(taken_places)` – остались ли свободные места;
- `validate_max_places()` – `@staticmethod`, проверка количества мест;
- `__str__()` – строковое представление.

### Participant – участник (`models/participants.py`)

Атрибуты: `id`, `name`, `email`, `phone`, `birth_date`.

Методы:

- `age_on(on_date)` – возраст участника на дату;
- `from_data(data)` – `@classmethod`, создание объекта из данных JSON;
- `__str__()` – строковое представление.

### Application – заявка (`models/applications.py`)

Атрибуты: `id`, `festival` (объект `Festival`), `participant`
(объект `Participant`), `status`.

Статус хранится в закрытом атрибуте `_status` и доступен только для чтения
через `@property status` (инкапсуляция). Изменить его можно только методами:

- `approve()` – одобрить;
- `reject()` – отклонить;
- `cancel()` – отменить;
- `is_active` – `@property`, занимает ли заявка место;
- `__str__()` – строковое представление.

## Взаимодействие объектов

```text
Application
├── festival    → Festival
├── participant → Participant
└── status
```

Заявка хранит ссылки на объекты фестиваля и участника, поэтому их данные
доступны напрямую: `application.festival.name`,
`application.participant.email`. Коллекции приложения:
`List[Festival]`, `List[Participant]`, `List[Application]`.

Функции работы с коллекциями остаются обычными функциями модулей:
`add_festival()`, `find_festivals()`, `find_festival_by_id()`,
`filter_upcoming_festivals()`, `sort_festivals()`, `add_participant()`,
`find_participants()`, `find_participant_by_id()`, `create_application()`,
`find_application_by_id()`, `change_application_status()`,
`cancel_application()`, `count_taken_places()`, `get_statistics()`.
Функция `check_application_possibility()` из ПР1 сохранена и используется
при создании заявки.

## Хранение данных

Данные хранятся в `data/festivals.json`, `data/participants.json`,
`data/applications.json`. При загрузке записи JSON преобразуются в объекты,
при сохранении – обратно в словари (модуль `storage.py`). В файле заявок
вместо объектов хранятся идентификаторы `festival_id` и `participant_id`;
при загрузке по ним восстанавливаются ссылки на объекты.

```json
{"id": 1, "festival_id": 1, "participant_id": 1, "status": "Одобрена"}
```

Отсутствующий или повреждённый файл и некорректные записи не приводят к
аварийному завершению программы.

## Веб-интерфейс (Django)

Django-проект `festival_site` (настройки, корневые маршруты) и три
Django-приложения:

| Приложение | Назначение |
|---|---|
| `homepage` | главная страница, обработчик 404, общие статические файлы |
| `festivals` | страницы фестивалей |
| `applications` | страницы заявок |

Отдельное приложение для участников пока не создаётся: работа с
пользователями (регистрация, вход) будет реализована вместе с
аутентификацией Django.

| URL | Имя маршрута | View-функция | Шаблон |
|---|---|---|---|
| `/` | `homepage:index` | `homepage.views.index()` | `homepage/index.html` |
| `/festivals/` | `festivals:list` | `festivals.views.festivals()` | `festivals/festival_list.html` |
| `/festivals/<int:festival_id>/` | `festivals:detail` | `festivals.views.festival_detail()` | `festivals/festival_detail.html` |
| `/applications/` | `applications:list` | `applications.views.applications()` | `applications/application_list.html` |
| `/applications/<int:application_id>/` | `applications:detail` | `applications.views.application_detail()` | `applications/application_detail.html` |

Если фестиваль или заявка с указанным идентификатором не найдены, шаблон
выводит сообщение «не найден(а)», а view-функция передаёт в `render()`
параметр `status=404`. Для адресов, которым не соответствует ни один
маршрут, настроен обработчик `handler404 = "homepage.views.page_not_found"`
(шаблон `homepage/404.html`, виден при `DEBUG = False`).

View-функции не формируют HTML и не дублируют логику предметной области:
они загружают данные функцией `storage.load_data()`, находят объекты
функциями `find_festival_by_id()` и `find_application_by_id()`, используют
методы `Festival.is_registration_open()`, `Festival.has_free_places()` и
функции `count_taken_places()`, `get_statistics()` из ПР3, складывают
результат в словарь контекста и вызывают
`render(request, "имя_шаблона.html", context)`. Функция `page()` из ПР5
удалена. Текстовые данные экранируются шаблонизатором автоматически.

## Шаблоны Django (ПР6)

### Базовый шаблон и наследование

`templates/base.html` (каталог шаблонов уровня проекта, подключён через
`TEMPLATES["DIRS"] = [BASE_DIR / "templates"]`) содержит общую структуру
страницы: `<head>`, Bootstrap, собственный CSS, шапку с логотипом,
навигацию, контейнер `<main>`, подвал и подключение JavaScript. Блоки:

```django
{% block title %}Фестивали{% endblock %}
{% block content %}{% endblock %}
```

Все страницы наследуют его: `{% extends "base.html" %}`.

### Включаемые шаблоны

| Шаблон | Назначение |
|---|---|
| `templates/includes/navigation.html` | навигация сайта |
| `festivals/includes/festival_card.html` | карточка фестиваля в списке |
| `applications/includes/application_status.html` | бейдж статуса заявки (в списке заявок, карточке заявки и на странице фестиваля) |

Подключение: `{% include "festivals/includes/festival_card.html" %}`.

### Контекст, циклы и условия

Например, список фестивалей получает `{"items": [...]}`, где для каждого
фестиваля view заранее вычисляет свободные места и признаки
`is_open`/`has_places`; шаблон перебирает их циклом
`{% for item in items %} ... {% empty %} ... {% endfor %}` и через
`{% if %} / {% elif %} / {% else %}` выбирает бейдж «завершён», «мест нет»
или «приём заявок». Статус заявки выводится по `application.is_active`.
Пустые коллекции обрабатываются через `{% empty %}`, отсутствие объекта –
через `{% if festival %}` / `{% if application %}`.

### Именованные URL и пространства имён

В `urls.py` приложений заданы `app_name` (`homepage`, `festivals`,
`applications`) и имена маршрутов (`index`, `list`, `detail`). Ссылки в
шаблонах формируются только через `{% url %}`:

```django
{% url 'festivals:list' %}
{% url 'festivals:detail' item.festival.id %}
{% url 'applications:detail' application.id %}
```

### Фильтры

- `{{ items|length }}`, `{{ applications|length }}` – количество элементов;
- `{{ festival.festival_date|date:"d.m.Y" }}` – формат даты;
- `{{ festival.name|default:"Без названия" }}`,
  `{{ participant.phone|default:"телефон не указан" }}` – значение по умолчанию;
- `{{ application.festival.name|truncatechars:40 }}` – сокращение длинного названия;
- `{{ participant.email|lower }}` – нижний регистр.

Фильтры только форматируют вывод, бизнес-логика остаётся в Python.

### Статические файлы

Каталог `homepage/static/homepage/`:

- `css/style.css` – собственные стили: шапка, навигация, карточки
  фестивалей (`.festival-card`, `.festival-card-closed`), статусы заявок
  (`.application-status-*`), подвал;
- `js/main.js` – выводит текущий год в подвале и подсвечивает пункт меню
  текущего раздела;
- `img/logo.png` – логотип в шапке.

Подключение в `base.html`: `{% load static %}` и
`{% static 'homepage/css/style.css' %}`.

На данном этапе веб-интерфейс только отображает данные. Данные по-прежнему
хранятся в JSON, Django ORM и формы ещё не используются. Добавление
фестивалей, регистрация участников, подача, одобрение и отмена заявок
доступны в консольной версии и появятся в вебе вместе с формами Django.

## Структура проекта

```text
festival_registration/
├── README.md
├── requirements.txt
├── manage.py          – управление Django-проектом
├── main.py            – консольная версия: меню и сценарии
├── storage.py         – загрузка и сохранение: JSON <-> объекты
├── validators.py      – проверка email, телефона, даты рождения (из ПР1)
├── utils.py           – безопасный ввод и вспомогательные функции
├── festival_site/     – настройки Django-проекта
│   ├── settings.py
│   ├── urls.py          – корневые маршруты и handler404
│   ├── asgi.py
│   └── wsgi.py
├── templates/         – шаблоны уровня проекта
│   ├── base.html        – базовый шаблон
│   └── includes/
│       └── navigation.html
├── homepage/          – Django-приложение: главная, 404, статика
│   ├── static/homepage/
│   │   ├── css/style.css
│   │   ├── js/main.js
│   │   └── img/logo.png
│   ├── templates/homepage/
│   │   ├── index.html
│   │   └── 404.html
│   ├── urls.py
│   └── views.py
├── festivals/         – Django-приложение: страницы фестивалей
│   ├── templates/festivals/
│   │   ├── festival_list.html
│   │   ├── festival_detail.html
│   │   └── includes/festival_card.html
│   ├── urls.py
│   └── views.py
├── applications/      – Django-приложение: страницы заявок
│   ├── templates/applications/
│   │   ├── application_list.html
│   │   ├── application_detail.html
│   │   └── includes/application_status.html
│   ├── urls.py
│   └── views.py
├── models/            – классы предметной области (ПР3)
│   ├── __init__.py
│   ├── festivals.py     – класс Festival и функции фестивалей
│   ├── participants.py  – класс Participant и функции участников
│   └── applications.py  – класс Application и функции заявок
├── data/
│   ├── festivals.json
│   ├── participants.json
│   └── applications.json
└── tests/
    ├── test_festivals.py
    ├── test_participants.py
    ├── test_applications.py
    ├── test_storage.py
    └── test_validators.py
```

## Запуск

Установка зависимостей:

```text
pip install -r requirements.txt
```

Веб-версия:

```text
python manage.py migrate
python manage.py runserver
```

После запуска открыть в браузере http://127.0.0.1:8000/

Консольная версия:

```text
python main.py
```

## Тестирование

```text
pytest -v
```

Тесты проверяют создание объектов и их атрибуты, методы классов, строковое
представление, операции с коллекциями, связь заявки с фестивалем и
участником, правила подачи заявки и преобразование JSON <-> объекты.

## Проверка качества кода

```text
flake8 . --extend-exclude=venv
```

## План развития

- перенос сущностей в Django ORM и подключение базы данных;
- формы подачи и обработки заявок в веб-интерфейсе;
- регистрация и вход пользователей;
- разработка API;
- контейнеризация (Docker) и CI/CD.
