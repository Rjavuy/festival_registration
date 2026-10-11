"""Точка запуска: консольное меню системы регистрации на фестивали."""

from datetime import date
from pathlib import Path

from applications import (
    STATUS_APPROVED,
    STATUS_REJECTED,
    cancel_application,
    count_taken_places,
    create_application,
    get_statistics,
    set_application_status,
)
from festivals import (
    add_festival,
    filter_upcoming_festivals,
    find_festivals,
    sort_festivals,
)
from participants import add_participant, find_participants
from storage import (
    load_applications,
    load_festivals,
    load_participants,
    save_applications,
    save_festivals,
    save_participants,
)
from utils import DATE_FORMAT, input_date, input_int, input_text

DATA_DIR = Path(__file__).parent / "data"
FESTIVALS_FILE = DATA_DIR / "festivals.json"
PARTICIPANTS_FILE = DATA_DIR / "participants.json"
APPLICATIONS_FILE = DATA_DIR / "applications.json"

MENU = """
=== Регистрация участников фестиваля ===
1. Показать фестивали
2. Найти фестиваль по названию
3. Предстоящие фестивали
4. Добавить фестиваль
5. Показать участников
6. Зарегистрировать участника
7. Найти участника
8. Подать заявку
9. Показать заявки
10. Одобрить / отклонить заявку
11. Отменить заявку
12. Статистика заявок
0. Выход"""


def show_festivals(festivals: list[dict], applications: list[dict]) -> None:
    """Вывести фестивали с количеством свободных мест."""
    if not festivals:
        print("Фестивали не найдены.")
        return
    for festival in festivals:
        free = festival["max_places"] - count_taken_places(
            applications, festival["id"]
        )
        print(
            f"{festival['id']:>3}. {festival['name']} | "
            f"{festival['festival_date'].strftime(DATE_FORMAT)} | "
            f"свободно {free} из {festival['max_places']}"
        )


def show_participants(participants: list[dict]) -> None:
    """Вывести список участников."""
    if not participants:
        print("Участники не найдены.")
        return
    for participant in participants:
        print(
            f"{participant['id']:>3}. {participant['name']} | "
            f"{participant['email']} | {participant['phone']}"
        )


def show_applications(
    applications: list[dict],
    festivals: dict[int, dict],
    participants: dict[int, dict],
) -> None:
    """Вывести заявки с названием фестиваля и именем участника."""
    if not applications:
        print("Заявок пока нет.")
        return
    for application in applications:
        festival = festivals.get(application["festival_id"])
        participant = participants.get(application["participant_id"])
        festival_name = festival["name"] if festival else "?"
        participant_name = participant["name"] if participant else "?"
        print(
            f"{application['id']:>3}. {participant_name} -> "
            f"{festival_name} | {application['status']}"
        )


def show_statistics(applications: list[dict]) -> None:
    """Вывести количество заявок по статусам."""
    statistics = get_statistics(applications)
    print(f"Всего заявок: {len(applications)}")
    for status, count in sorted(statistics.items()):
        print(f"  {status}: {count}")


def register_participant(participants: dict[int, dict]) -> bool:
    """Сценарий регистрации участника; True, если участник добавлен."""
    name = input_text("Имя и фамилия: ")
    email = input_text("Email: ")
    phone = input_text("Телефон (+7XXXXXXXXXX или 8XXXXXXXXXX): ")
    birth_date = input_date("Дата рождения (ДД.ММ.ГГГГ): ")
    try:
        participant_id = add_participant(
            participants, name, email, phone,
            birth_date.isoformat(), date.today(),
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return False
    print(f"Участник зарегистрирован, id = {participant_id}")
    return True


def submit_application(
    applications: list[dict],
    festivals: dict[int, dict],
    participants: dict[int, dict],
) -> bool:
    """Сценарий подачи заявки; True, если заявка создана."""
    participant_id = input_int("ID участника: ")
    festival_id = input_int("ID фестиваля: ")
    try:
        application = create_application(
            applications, festivals, participants,
            participant_id, festival_id, date.today(),
        )
    except KeyError as error:
        print(f"Ошибка: {error.args[0]}")
        return False
    except ValueError as error:
        print(f"Заявка не принята. {error}")
        return False
    print(f"Заявка №{application['id']}: {application['status']}")
    return True


def review_application(applications: list[dict]) -> bool:
    """Сценарий решения организатора по заявке."""
    application_id = input_int("ID заявки: ")
    choice = input_int("1 - одобрить, 2 - отклонить: ", min_value=1)
    status = STATUS_APPROVED if choice == 1 else STATUS_REJECTED
    if set_application_status(applications, application_id, status):
        print(f"Статус заявки изменён: {status}")
        return True
    print("Активная заявка с таким ID не найдена.")
    return False


def main() -> None:
    """Загрузить данные и запустить цикл меню."""
    festivals = load_festivals(FESTIVALS_FILE)
    participants = load_participants(PARTICIPANTS_FILE)
    applications = load_applications(APPLICATIONS_FILE)

    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        changed = False

        if choice == "1":
            show_festivals(sort_festivals(festivals), applications)
        elif choice == "2":
            query = input_text("Часть названия: ")
            show_festivals(find_festivals(festivals, query), applications)
        elif choice == "3":
            upcoming = filter_upcoming_festivals(festivals, date.today())
            show_festivals(
                sorted(upcoming, key=lambda f: f["festival_date"]),
                applications,
            )
        elif choice == "4":
            name = input_text("Название: ")
            festival_date = input_date("Дата проведения (ДД.ММ.ГГГГ): ")
            max_places = input_int("Количество мест: ", min_value=1)
            festival_id = add_festival(
                festivals, name, festival_date, max_places
            )
            print(f"Фестиваль добавлен, id = {festival_id}")
            changed = True
        elif choice == "5":
            show_participants(list(participants.values()))
        elif choice == "6":
            changed = register_participant(participants)
        elif choice == "7":
            query = input_text("Имя или email: ")
            show_participants(find_participants(participants, query))
        elif choice == "8":
            changed = submit_application(
                applications, festivals, participants
            )
        elif choice == "9":
            show_applications(applications, festivals, participants)
        elif choice == "10":
            changed = review_application(applications)
        elif choice == "11":
            application_id = input_int("ID заявки: ")
            changed = cancel_application(applications, application_id)
            print("Заявка отменена." if changed else "Заявка не найдена.")
        elif choice == "12":
            show_statistics(applications)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Нет такого пункта меню.")

        if changed:
            save_festivals(FESTIVALS_FILE, festivals)
            save_participants(PARTICIPANTS_FILE, participants)
            save_applications(APPLICATIONS_FILE, applications)


if __name__ == "__main__":
    main()
