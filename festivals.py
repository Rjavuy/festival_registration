"""Функции для работы с фестивалями."""

from datetime import date
from typing import Iterator

from utils import next_id


def add_festival(
    festivals: dict[int, dict],
    name: str,
    festival_date: date,
    max_places: int,
) -> int:
    """Добавить фестиваль в словарь festivals и вернуть его id.

    Возбуждает ValueError, если название пустое или мест меньше одного.
    """
    if not name.strip():
        raise ValueError("Название фестиваля не может быть пустым")
    if max_places < 1:
        raise ValueError("Количество мест должно быть больше нуля")
    festival_id = next_id(festivals)
    festivals[festival_id] = {
        "id": festival_id,
        "name": name.strip(),
        "festival_date": festival_date,
        "max_places": max_places,
    }
    return festival_id


def find_festivals(festivals: dict[int, dict], query: str) -> list[dict]:
    """Найти фестивали, в названии которых встречается подстрока query."""
    query = query.lower()
    return [
        festival for festival in festivals.values()
        if query in festival["name"].lower()
    ]


def filter_upcoming_festivals(
    festivals: dict[int, dict],
    current_date: date,
) -> Iterator[dict]:
    """Отобрать фестивали, которые ещё не прошли (генератор)."""
    for festival in festivals.values():
        if festival["festival_date"] >= current_date:
            yield festival


def sort_festivals(
    festivals: dict[int, dict],
    by: str = "date",
) -> list[dict]:
    """Отсортировать фестивали по дате ("date") или названию ("name")."""
    if by == "name":
        return sorted(festivals.values(), key=lambda f: f["name"].lower())
    return sorted(festivals.values(), key=lambda f: f["festival_date"])
