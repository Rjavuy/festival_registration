# Система регистрации участников фестиваля

## Назначение

Консольное приложение для автоматизации подачи и обработки заявок на участие
в фестивалях. Участники регистрируются и подают заявки, организаторы
проверяют их и присваивают статус.

## Целевая аудитория

- Участники фестиваля (артисты, волонтёры, гости).
- Организаторы и администраторы фестиваля.

## Предметная область

Организация и проведение массовых мероприятий (фестивалей).

Основные сущности: фестиваль, участник, заявка, статус заявки.

Правила подачи заявки:

- участнику должно быть не меньше 14 лет;
- заявку можно подать не позже даты проведения фестиваля;
- на фестивале должны быть свободные места (их занимают заявки со статусами
  «Отправлена» и «Одобрена»);
- участник не может подать две активные заявки на один фестиваль.

## Возможности

- просмотр фестивалей со свободными местами (сортировка по дате);
- поиск фестиваля по названию;
- отбор предстоящих фестивалей;
- добавление фестиваля;
- регистрация участника с проверкой email, телефона и даты рождения;
- поиск участника по имени или email;
- подача заявки с проверкой возможности участия;
- одобрение и отклонение заявки организатором;
- отмена заявки (запись сохраняется со статусом «Отменена»);
- статистика заявок по статусам;
- сохранение данных в JSON между запусками.

## Структура проекта

```text
festival_registration/
├── README.md
├── requirements.txt
├── main.py            – точка запуска, меню и пользовательские сценарии
├── festivals.py       – функции работы с фестивалями
├── participants.py    – функции работы с участниками
├── applications.py    – подача, проверка и обработка заявок
├── validators.py      – проверка email, телефона, даты рождения (из ПР1)
├── storage.py         – загрузка и сохранение JSON-файлов
├── utils.py           – безопасный ввод и вспомогательные функции
├── data/
│   ├── festivals.json
│   ├── participants.json
│   └── applications.json
└── tests/             – автоматизированные тесты pytest
```

## Функции проекта

| Модуль | Функции |
|---|---|
| `main.py` | `main()`, `show_festivals()`, `show_participants()`, `show_applications()`, `show_statistics()`, `register_participant()`, `submit_application()`, `review_application()` |
| `festivals.py` | `add_festival()`, `find_festivals()`, `filter_upcoming_festivals()` (генератор), `sort_festivals()` (lambda) |
| `participants.py` | `add_participant()`, `find_participants()` |
| `applications.py` | `check_application_possibility()` (из ПР1), `count_taken_places()`, `has_active_application()`, `create_application()`, `find_application()`, `set_application_status()`, `cancel_application()`, `get_statistics()` |
| `validators.py` | `validate_email()`, `validate_phone()`, `validate_birth_date()` (из ПР1) |
| `storage.py` | `load_list()` / `save_list()`, `load_festivals()` / `save_festivals()`, `load_participants()` / `save_participants()`, `load_applications()` / `save_applications()` |
| `utils.py` | `input_text()`, `input_int()`, `input_date()`, `parse_date()`, `calculate_age()`, `next_id()` |

## Формат данных

В программе фестивали и участники хранятся в словарях `{id: данные}`,
заявки – в списке словарей. В файлах данные хранятся списками,
даты – в формате ISO (`ГГГГ-ММ-ДД`).

`data/festivals.json`:

```json
[
    {"id": 1, "name": "Городской фестиваль искусств",
     "festival_date": "2026-12-15", "max_places": 100}
]
```

`data/participants.json`:

```json
[
    {"id": 1, "name": "Иван Петров", "email": "ivan.petrov@example.com",
     "phone": "+79161234567", "birth_date": "2000-05-15"}
]
```

`data/applications.json`:

```json
[
    {"id": 1, "festival_id": 1, "participant_id": 1, "status": "Одобрена"}
]
```

Если файл отсутствует или повреждён, программа не завершается аварийно:
выводится сообщение и используется пустой набор данных.

## Требования

- Python 3.10+;
- pytest;
- flake8.

Установка зависимостей:

```text
pip install -r requirements.txt
```

## Запуск программы

```text
python main.py
```

## Запуск тестов

```text
pytest
```

## Проверка качества кода

```text
flake8
```

## План развития

- ПР3 – переход к объектной модели (классы фестиваля, участника, заявки);
- веб-приложение на Django;
- подключение базы данных;
- разработка API;
- контейнеризация (Docker) и CI/CD.
