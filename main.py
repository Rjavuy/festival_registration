"""Точка запуска: консольное меню системы регистрации на фестивали."""

from datetime import date
from pathlib import Path
from typing import List

from models import Application, Festival, Participant
from models.applications import (
    cancel_application,
    change_application_status,
    count_taken_places,
    create_application,
    get_statistics,
)
from models.festivals import (
    add_festival,
    filter_upcoming_festivals,
    find_festival_by_id,
    find_festivals,
    sort_festivals,
)
from models.participants import (
    add_participant,
    find_participant_by_id,
    find_participants,
)
from storage import (
    load_applications,
    load_festivals,
    load_participants,
    save_applications,
    save_festivals,
    save_participants,
)
from utils import input_date, input_int, input_text

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


def show_festivals(
    festivals: List[Festival],
    applications: List[Application],
) -> None:
    """Вывести фестивали с количеством свободных мест."""
    if not festivals:
        print("Фестивали не найдены.")
        return
    for festival in festivals:
        free = festival.max_places - count_taken_places(
            applications, festival
        )
        print(f"{festival.id:>3}. {festival} | свободно {free}")


def show_participants(participants: List[Participant]) -> None:
    """Вывести список участников."""
    if not participants:
        print("Участники не найдены.")
        return
    for participant in participants:
        print(f"{participant.id:>3}. {participant} | {participant.phone}")


def show_applications(applications: List[Application]) -> None:
    """Вывести список заявок."""
    if not applications:
        print("Заявок пока нет.")
        return
    for application in applications:
        print(application)


def show_statistics(applications: List[Application]) -> None:
    """Вывести количество заявок по статусам."""
    print(f"Всего заявок: {len(applications)}")
    for status, count in sorted(get_statistics(applications).items()):
        print(f"  {status}: {count}")


def create_new_festival(festivals: List[Festival]) -> bool:
    """Сценарий добавления фестиваля."""
    name = input_text("Название: ")
    festival_date = input_date("Дата проведения (ДД.ММ.ГГГГ): ")
    max_places = input_int("Количество мест: ", min_value=1)
    festival = add_festival(festivals, name, festival_date, max_places)
    print(f"Фестиваль добавлен, id = {festival.id}")
    return True


def register_participant(participants: List[Participant]) -> bool:
    """Сценарий регистрации участника; True, если участник добавлен."""
    name = input_text("Имя и фамилия: ")
    email = input_text("Email: ")
    phone = input_text("Телефон (+7XXXXXXXXXX или 8XXXXXXXXXX): ")
    birth_date = input_date("Дата рождения (ДД.ММ.ГГГГ): ")
    try:
        participant = add_participant(
            participants, name, email, phone,
            birth_date.isoformat(), date.today(),
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return False
    print(f"Участник зарегистрирован, id = {participant.id}")
    return True


def submit_application(
    applications: List[Application],
    festivals: List[Festival],
    participants: List[Participant],
) -> bool:
    """Сценарий подачи заявки: поиск объектов, проверка, создание."""
    participant = find_participant_by_id(
        participants, input_int("ID участника: ")
    )
    if participant is None:
        print("Участник не найден.")
        return False
    festival = find_festival_by_id(festivals, input_int("ID фестиваля: "))
    if festival is None:
        print("Фестиваль не найден.")
        return False
    try:
        application = create_application(
            applications, festival, participant, date.today()
        )
    except ValueError as error:
        print(f"Заявка не принята. {error}")
        return False
    print(application)
    return True


def review_application(applications: List[Application]) -> bool:
    """Сценарий решения организатора по заявке."""
    application_id = input_int("ID заявки: ")
    choice = input_int("1 - одобрить, 2 - отклонить: ", min_value=1)
    action = Application.approve if choice == 1 else Application.reject
    if change_application_status(applications, application_id, action):
        print("Статус заявки изменён.")
        return True
    print("Активная заявка с таким ID не найдена.")
    return False


def main() -> None:
    """Загрузить данные и запустить цикл меню."""
    festivals = load_festivals(FESTIVALS_FILE)
    participants = load_participants(PARTICIPANTS_FILE)
    applications = load_applications(
        APPLICATIONS_FILE, festivals, participants
    )

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
                sorted(upcoming, key=lambda f: f.festival_date),
                applications,
            )
        elif choice == "4":
            changed = create_new_festival(festivals)
        elif choice == "5":
            show_participants(participants)
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
            show_applications(applications)
        elif choice == "10":
            changed = review_application(applications)
        elif choice == "11":
            application_id = input_int("ID заявки: ")
            changed = cancel_application(applications, application_id)
            print(
                "Заявка отменена." if changed
                else "Активная заявка с таким ID не найдена."
            )
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
