from datetime import date

from validators import validate_birth_date, validate_email, validate_phone


def test_validate_email():
    assert validate_email("user@example.com")
    assert not validate_email("user.example.com")
    assert not validate_email("user@example")


def test_validate_phone():
    assert validate_phone("+79161234567")
    assert validate_phone("89161234567")
    assert not validate_phone("+7916123")


def test_validate_birth_date():
    today = date(2026, 9, 27)
    assert validate_birth_date("2000-05-15", today)
    assert not validate_birth_date("2015-01-01", today)
    assert not validate_birth_date("15.05.2000", today)
