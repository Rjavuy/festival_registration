from datetime import date

import pytest

from models import Participant
from models.participants import add_participant, find_participants

TODAY = date(2026, 9, 27)


def test_participant_creation():
    participant = Participant(
        1, "Иван Петров", "ivan@example.com", "+79161234567",
        date(2000, 5, 15),
    )
    assert participant.id == 1
    assert participant.name == "Иван Петров"
    assert participant.email == "ivan@example.com"
    assert str(participant) == "Иван Петров <ivan@example.com>"


def test_participant_age():
    participant = Participant(
        1, "Иван", "ivan@example.com", "+79161234567", date(2000, 9, 28),
    )
    assert participant.age_on(TODAY) == 25


def test_participant_from_data():
    participant = Participant.from_data({
        "id": 2,
        "name": "Анна",
        "email": "anna@example.com",
        "phone": "89031112233",
        "birth_date": "2004-11-02",
    })
    assert participant.id == 2
    assert participant.birth_date == date(2004, 11, 2)


def test_add_and_find_participant():
    participants = []
    add_participant(participants, "Иван Петров", "ivan@example.com",
                    "+79161234567", "2000-05-15", TODAY)
    add_participant(participants, "Анна Смирнова", "anna@example.com",
                    "89031112233", "2004-11-02", TODAY)
    assert [p.id for p in find_participants(participants, "анна")] == [2]
    assert [p.id for p in find_participants(participants, "ivan@")] == [1]


def test_add_participant_invalid_data():
    participants = []
    with pytest.raises(ValueError, match="email"):
        add_participant(participants, "Иван", "bad-email",
                        "+79161234567", "2000-05-15", TODAY)
    with pytest.raises(ValueError, match="14"):
        add_participant(participants, "Петя", "petya@example.com",
                        "+79161234567", "2015-01-01", TODAY)
    assert participants == []
