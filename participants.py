"""Функции для работы с участниками фестиваля."""

from datetime import date

from utils import next_id
from validators import validate_birth_date, validate_email, validate_phone


def add_participant(
    participants: dict[int, dict],
    name: str,
    email: str,
    phone: str,
    birth_date_str: str,
    current_date: date,
) -> int:
    """Зарегистрировать участника и вернуть его id.

    Данные проверяются функциями из validators.py;
    при ошибке возбуждается ValueError с описанием причины.
    """
    if not name.strip():
        raise ValueError("Имя участника не может быть пустым")
    if not validate_email(email):
        raise ValueError("Некорректный email")
    if not validate_phone(phone):
        raise ValueError("Некорректный телефон")
    if not validate_birth_date(birth_date_str, current_date):
        raise ValueError(
            "Некорректная дата рождения или участнику меньше 14 лет"
        )
    if any(p["email"] == email for p in participants.values()):
        raise ValueError("Участник с таким email уже зарегистрирован")
    participant_id = next_id(participants)
    participants[participant_id] = {
        "id": participant_id,
        "name": name.strip(),
        "email": email,
        "phone": phone,
        "birth_date": date.fromisoformat(birth_date_str),
    }
    return participant_id


def find_participants(
    participants: dict[int, dict],
    query: str,
) -> list[dict]:
    """Найти участников по подстроке имени или email."""
    query = query.lower()
    return [
        participant for participant in participants.values()
        if query in participant["name"].lower()
        or query in participant["email"].lower()
    ]
