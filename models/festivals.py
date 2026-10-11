"""Класс Festival и функции работы с коллекцией фестивалей."""

from datetime import date
from typing import Iterator, List, Optional

from utils import DATE_FORMAT, next_id


class Festival:
    """Фестиваль, на который участники подают заявки."""

    def __init__(
        self,
        festival_id: int,
        name: str,
        festival_date: date,
        max_places: int,
    ) -> None:
        """Создать фестиваль; ValueError при некорректных данных."""
        if not name.strip():
            raise ValueError("Название фестиваля не может быть пустым")
        if not Festival.validate_max_places(max_places):
            raise ValueError("Количество мест должно быть больше нуля")
        self.id = festival_id
        self.name = name.strip()
        self.festival_date = festival_date
        self.max_places = max_places

    @staticmethod
    def validate_max_places(max_places: int) -> bool:
        """Проверить корректность количества мест."""
        return max_places >= 1

    def is_registration_open(self, current_date: date) -> bool:
        """Проверить, принимаются ли заявки на дату current_date."""
        return current_date <= self.festival_date

    def has_free_places(self, taken_places: int) -> bool:
        """Проверить, остались ли свободные места."""
        return taken_places < self.max_places

    def __str__(self) -> str:
        """Вернуть строковое представление фестиваля."""
        return (
            f"{self.name} ({self.festival_date.strftime(DATE_FORMAT)}, "
            f"мест: {self.max_places})"
        )


def add_festival(
    festivals: List[Festival],
    name: str,
    festival_date: date,
    max_places: int,
) -> Festival:
    """Создать фестиваль, добавить его в коллекцию и вернуть."""
    festival = Festival(
        next_id(f.id for f in festivals), name, festival_date, max_places
    )
    festivals.append(festival)
    return festival


def find_festival_by_id(
    festivals: List[Festival],
    festival_id: int,
) -> Optional[Festival]:
    """Найти фестиваль по идентификатору."""
    for festival in festivals:
        if festival.id == festival_id:
            return festival
    return None


def find_festivals(festivals: List[Festival], query: str) -> List[Festival]:
    """Найти фестивали, в названии которых встречается подстрока query."""
    query = query.lower()
    return [f for f in festivals if query in f.name.lower()]


def filter_upcoming_festivals(
    festivals: List[Festival],
    current_date: date,
) -> Iterator[Festival]:
    """Отобрать фестивали, на которые ещё принимаются заявки (генератор)."""
    for festival in festivals:
        if festival.is_registration_open(current_date):
            yield festival


def sort_festivals(
    festivals: List[Festival],
    by: str = "date",
) -> List[Festival]:
    """Отсортировать фестивали по дате ("date") или названию ("name")."""
    if by == "name":
        return sorted(festivals, key=lambda f: f.name.lower())
    return sorted(festivals, key=lambda f: f.festival_date)
