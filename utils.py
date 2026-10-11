"""Вспомогательные функции: безопасный ввод и общие вычисления."""

from datetime import date, datetime
from typing import Iterable, Optional

DATE_FORMAT = "%d.%m.%Y"


def next_id(ids: Iterable[int]) -> int:
    """Вернуть следующий свободный идентификатор."""
    return max(ids, default=0) + 1


def calculate_age(birth_date: date, on_date: date) -> int:
    """Вычислить полный возраст на дату on_date."""
    age = on_date.year - birth_date.year
    if (on_date.month, on_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def parse_date(text: str) -> date:
    """Преобразовать строку ДД.ММ.ГГГГ в дату (ValueError при ошибке)."""
    return datetime.strptime(text.strip(), DATE_FORMAT).date()


def input_text(prompt: str) -> str:
    """Запросить непустую строку; при пустом вводе повторить запрос."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Значение не может быть пустым.")


def input_int(prompt: str, min_value: Optional[int] = None) -> int:
    """Запросить целое число; при некорректном вводе повторить запрос."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Введите целое число.")
            continue
        if min_value is not None and value < min_value:
            print(f"Число должно быть не меньше {min_value}.")
            continue
        return value


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ; при ошибке повторить запрос."""
    while True:
        try:
            return parse_date(input(prompt))
        except ValueError:
            print("Неверный формат даты. Пример: 15.12.2026")
