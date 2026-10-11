"""Класс Participant и функции работы с коллекцией участников."""

from datetime import date
from typing import List, Optional

from utils import calculate_age, next_id
from validators import validate_birth_date, validate_email, validate_phone


class Participant:
    """Участник фестиваля."""

    def __init__(
        self,
        participant_id: int,
        name: str,
        email: str,
        phone: str,
        birth_date: date,
    ) -> None:
        """Создать участника."""
        self.id = participant_id
        self.name = name
        self.email = email
        self.phone = phone
        self.birth_date = birth_date

    @classmethod
    def from_data(cls, data: dict) -> "Participant":
        """Создать участника из словаря, прочитанного из JSON."""
        return cls(
            participant_id=data["id"],
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            birth_date=date.fromisoformat(data["birth_date"]),
        )

    def age_on(self, on_date: date) -> int:
        """Вернуть полный возраст участника на дату on_date."""
        return calculate_age(self.birth_date, on_date)

    def __str__(self) -> str:
        """Вернуть строковое представление участника."""
        return f"{self.name} <{self.email}>"


def add_participant(
    participants: List[Participant],
    name: str,
    email: str,
    phone: str,
    birth_date_str: str,
    current_date: date,
) -> Participant:
    """Проверить данные, создать участника и добавить его в коллекцию.

    При некорректных данных возбуждается ValueError с описанием причины.
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
    if any(p.email == email for p in participants):
        raise ValueError("Участник с таким email уже зарегистрирован")
    participant = Participant(
        next_id(p.id for p in participants),
        name.strip(),
        email,
        phone,
        date.fromisoformat(birth_date_str),
    )
    participants.append(participant)
    return participant


def find_participant_by_id(
    participants: List[Participant],
    participant_id: int,
) -> Optional[Participant]:
    """Найти участника по идентификатору."""
    for participant in participants:
        if participant.id == participant_id:
            return participant
    return None


def find_participants(
    participants: List[Participant],
    query: str,
) -> List[Participant]:
    """Найти участников по подстроке имени или email."""
    query = query.lower()
    return [
        p for p in participants
        if query in p.name.lower() or query in p.email.lower()
    ]
