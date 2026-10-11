from datetime import date

import pytest

from models import Application, Festival, Participant
from models.applications import (
    STATUS_APPROVED,
    STATUS_CANCELLED,
    STATUS_SUBMITTED,
    cancel_application,
    change_application_status,
    check_application_possibility,
    create_application,
    get_statistics,
)

TODAY = date(2026, 9, 27)


def make_objects(max_places=100):
    festival = Festival(1, "Фестиваль искусств", date(2026, 12, 15),
                        max_places)
    ivan = Participant(1, "Иван", "ivan@example.com", "+79161234567",
                       date(2000, 5, 15))
    anna = Participant(2, "Анна", "anna@example.com", "89031112233",
                       date(2004, 11, 2))
    return festival, ivan, anna


def test_check_application_possibility():
    festival_date = date(2026, 12, 15)
    assert check_application_possibility(
        24, festival_date, TODAY, 100, 87) == STATUS_SUBMITTED
    assert "возраст" in check_application_possibility(
        12, festival_date, TODAY, 100, 87)
    assert "мест" in check_application_possibility(
        24, festival_date, TODAY, 100, 100)


def test_application_creation():
    festival, ivan, _ = make_objects()
    application = Application(1, festival, ivan)
    assert application.festival is festival
    assert application.participant is ivan
    assert application.status == STATUS_SUBMITTED
    assert application.is_active
    assert str(application) == (
        "Заявка №1: Иван -> Фестиваль искусств [Отправлена]"
    )


def test_application_cancel():
    festival, ivan, _ = make_objects()
    application = Application(1, festival, ivan)
    application.cancel()
    assert application.status == STATUS_CANCELLED
    assert not application.is_active
    with pytest.raises(ValueError):
        application.approve()


def test_status_is_read_only():
    festival, ivan, _ = make_objects()
    application = Application(1, festival, ivan)
    with pytest.raises(AttributeError):
        application.status = STATUS_APPROVED


def test_create_application():
    festival, ivan, _ = make_objects()
    applications = []
    application = create_application(applications, festival, ivan, TODAY)
    assert applications == [application]
    assert application.participant.email == "ivan@example.com"


def test_duplicate_application_forbidden():
    festival, ivan, _ = make_objects()
    applications = []
    create_application(applications, festival, ivan, TODAY)
    with pytest.raises(ValueError, match="уже подал"):
        create_application(applications, festival, ivan, TODAY)


def test_cancelled_application_frees_place():
    festival, ivan, anna = make_objects(max_places=1)
    applications = []
    create_application(applications, festival, ivan, TODAY)
    with pytest.raises(ValueError, match="мест нет"):
        create_application(applications, festival, anna, TODAY)
    assert cancel_application(applications, 1)
    create_application(applications, festival, anna, TODAY)
    assert len(applications) == 2


def test_statistics():
    festival, ivan, anna = make_objects()
    applications = []
    create_application(applications, festival, ivan, TODAY)
    create_application(applications, festival, anna, TODAY)
    assert change_application_status(applications, 1, Application.approve)
    assert not change_application_status(applications, 99, Application.reject)
    assert get_statistics(applications) == {
        STATUS_APPROVED: 1,
        STATUS_SUBMITTED: 1,
    }
