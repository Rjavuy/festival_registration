"""Проверка данных участника (функции перенесены из ПР1)."""

from datetime import date

from utils import calculate_age

MIN_AGE = 14


def validate_email(email: str) -> bool:
    """Проверить корректность email (наличие @ и точки в домене)."""
    if email.count("@") != 1:
        return False
    local_part, domain = email.split("@")
    return bool(local_part) and "." in domain and not domain.endswith(".")


def validate_phone(phone: str) -> bool:
    """Проверить телефон: +7XXXXXXXXXX или 8XXXXXXXXXX."""
    if len(phone) == 12 and phone.startswith("+7") and phone[2:].isdigit():
        return True
    if len(phone) == 11 and phone.startswith("8") and phone[1:].isdigit():
        return True
    return False


def validate_birth_date(birth_date_str: str, current_date: date) -> bool:
    """Проверить дату рождения (формат ГГГГ-ММ-ДД) и возраст >= 14."""
    try:
        birth_date = date.fromisoformat(birth_date_str)
    except ValueError:
        return False
    return calculate_age(birth_date, current_date) >= MIN_AGE
