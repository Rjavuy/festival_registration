from datetime import date


# Данные фестиваля (условные)
FESTIVAL_NAME = "Городской фестиваль искусств"
FESTIVAL_DATE = date(2026, 12, 15)
CURRENT_DATE = date(2026, 9, 27)
MAX_PLACES = 100
TAKEN_PLACES = 87


def validate_email(email):
    """Проверяет корректность email (наличие @ и .)."""
    if "@" in email and "." in email:
        return True
    return False


def validate_phone(phone):
    """Проверяет телефон: +7XXXXXXXXXX или 8XXXXXXXXXX."""
    if len(phone) == 12 and phone.startswith("+7") and phone[2:].isdigit():
        return True
    if len(phone) == 11 and phone.startswith("8") and phone[1:].isdigit():
        return True
    return False


def validate_birth_date(birth_date_str, current_date):
    """Проверяет дату рождения (формат ГГГГ-ММ-ДД) и возраст >= 14."""
    try:
        birth_date = date.fromisoformat(birth_date_str)
    except ValueError:
        return False
    age = current_date.year - birth_date.year
    if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age >= 14


def check_application_possibility(age, festival_date, current_date, max_places, taken_places):
    """Проверяет, может ли участник подать заявку."""
    if age > 14:
        return "Отклонена: возраст меньше 14 лет"
    if current_date > festival_date:
        return "Отклонена: дедлайн подачи заявок прошёл"
    if taken_places >= max_places:
        return "Отклонена: свободных мест нет"
    return "Отправлена"


if __name__ == "__main__":
    email = "user@example.com"
    phone = "+79161234567"
    birth_date_str = "2000-05-15"

    print(f"Фестиваль: {FESTIVAL_NAME}")
    print(f"Дата фестиваля: {FESTIVAL_DATE}")
    print(f"Свободных мест: {MAX_PLACES - TAKEN_PLACES}")

    print("\n--- Проверка данных ---")
    print(f"Email корректен: {validate_email(email)}")
    print(f"Телефон корректен: {validate_phone(phone)}")
    print(f"Дата рождения корректна: {validate_birth_date(birth_date_str, CURRENT_DATE)}")

    print("\n--- Проверка возможности подачи заявки ---")
    age = 24
    status = check_application_possibility(
        age, FESTIVAL_DATE, CURRENT_DATE, MAX_PLACES, TAKEN_PLACES
    )
    print(f"Статус заявки: {status}")