"""Функции для подачи, проверки и обработки заявок."""

from datetime import date
from typing import Optional

from utils import calculate_age, next_id
from validators import MIN_AGE

STATUS_SUBMITTED = "Отправлена"
STATUS_APPROVED = "Одобрена"
STATUS_REJECTED = "Отклонена"
STATUS_CANCELLED = "Отменена"

# Заявки с этими статусами занимают место на фестивале.
ACTIVE_STATUSES = {STATUS_SUBMITTED, STATUS_APPROVED}


def check_application_possibility(
    age: int,
    festival_date: date,
    current_date: date,
    max_places: int,
    taken_places: int,
) -> str:
    """Проверить, может ли участник подать заявку (функция из ПР1)."""
    if age < MIN_AGE:
        return "Отклонена: возраст меньше 14 лет"
    if current_date > festival_date:
        return "Отклонена: дедлайн подачи заявок прошёл"
    if taken_places >= max_places:
        return "Отклонена: свободных мест нет"
    return STATUS_SUBMITTED


def count_taken_places(applications: list[dict], festival_id: int) -> int:
    """Посчитать места, занятые активными заявками на фестиваль."""
    return sum(
        1 for application in applications
        if application["festival_id"] == festival_id
        and application["status"] in ACTIVE_STATUSES
    )


def has_active_application(
    applications: list[dict],
    participant_id: int,
    festival_id: int,
) -> bool:
    """Проверить, есть ли у участника активная заявка на фестиваль."""
    return any(
        application["participant_id"] == participant_id
        and application["festival_id"] == festival_id
        and application["status"] in ACTIVE_STATUSES
        for application in applications
    )


def create_application(
    applications: list[dict],
    festivals: dict[int, dict],
    participants: dict[int, dict],
    participant_id: int,
    festival_id: int,
    current_date: date,
) -> dict:
    """Создать заявку участника на фестиваль и добавить её в список.

    Возбуждает KeyError, если участник или фестиваль не найдены,
    и ValueError, если подать заявку нельзя (причина в тексте).
    """
    if festival_id not in festivals:
        raise KeyError(f"Фестиваль с id={festival_id} не найден")
    if participant_id not in participants:
        raise KeyError(f"Участник с id={participant_id} не найден")
    if has_active_application(applications, participant_id, festival_id):
        raise ValueError("Участник уже подал заявку на этот фестиваль")

    festival = festivals[festival_id]
    participant = participants[participant_id]
    status = check_application_possibility(
        calculate_age(participant["birth_date"], current_date),
        festival["festival_date"],
        current_date,
        festival["max_places"],
        count_taken_places(applications, festival_id),
    )
    if status != STATUS_SUBMITTED:
        raise ValueError(status)

    application = {
        "id": next_id(a["id"] for a in applications),
        "festival_id": festival_id,
        "participant_id": participant_id,
        "status": status,
    }
    applications.append(application)
    return application


def find_application(
    applications: list[dict],
    application_id: int,
) -> Optional[dict]:
    """Найти заявку по идентификатору."""
    for application in applications:
        if application["id"] == application_id:
            return application
    return None


def set_application_status(
    applications: list[dict],
    application_id: int,
    status: str,
) -> bool:
    """Изменить статус заявки (решение организатора или отмена).

    Менять можно только активную заявку; возвращает True при успехе.
    """
    application = find_application(applications, application_id)
    if application is None or application["status"] not in ACTIVE_STATUSES:
        return False
    application["status"] = status
    return True


def cancel_application(applications: list[dict], application_id: int) -> bool:
    """Отменить заявку: запись сохраняется со статусом «Отменена»."""
    return set_application_status(
        applications, application_id, STATUS_CANCELLED
    )


def get_statistics(applications: list[dict]) -> dict[str, int]:
    """Посчитать количество заявок по каждому статусу."""
    statistics: dict[str, int] = {}
    for application in applications:
        status = application["status"]
        statistics[status] = statistics.get(status, 0) + 1
    return statistics
