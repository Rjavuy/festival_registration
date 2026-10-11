from datetime import date

import pytest

from applications import (
    STATUS_APPROVED,
    STATUS_CANCELLED,
    STATUS_SUBMITTED,
    cancel_application,
    check_application_possibility,
    create_application,
    get_statistics,
    set_application_status,
)
from festivals import add_festival
from participants import add_participant

TODAY = date(2026, 9, 27)


def make_data(max_places=100):
    festivals = {}
    participants = {}
    add_festival(festivals, "Фестиваль искусств", date(2026, 12, 15),
                 max_places)
    add_participant(participants, "Иван", "ivan@example.com",
                    "+79161234567", "2000-05-15", TODAY)
    add_participant(participants, "Анна", "anna@example.com",
                    "89031112233", "2004-11-02", TODAY)
    return festivals, participants


def test_check_application_possibility():
    festival_date = date(2026, 12, 15)
    assert check_application_possibility(
        24, festival_date, TODAY, 100, 87) == STATUS_SUBMITTED
    assert "возраст" in check_application_possibility(
        12, festival_date, TODAY, 100, 87)
    assert "мест" in check_application_possibility(
        24, festival_date, TODAY, 100, 100)


def test_create_application():
    festivals, participants = make_data()
    applications = []
    application = create_application(
        applications, festivals, participants, 1, 1, TODAY)
    assert application["status"] == STATUS_SUBMITTED
    assert applications == [application]


def test_duplicate_application_forbidden():
    festivals, participants = make_data()
    applications = []
    create_application(applications, festivals, participants, 1, 1, TODAY)
    with pytest.raises(ValueError):
        create_application(
            applications, festivals, participants, 1, 1, TODAY)


def test_no_free_places():
    festivals, participants = make_data(max_places=1)
    applications = []
    create_application(applications, festivals, participants, 1, 1, TODAY)
    with pytest.raises(ValueError, match="мест нет"):
        create_application(
            applications, festivals, participants, 2, 1, TODAY)


def test_unknown_festival():
    festivals, participants = make_data()
    with pytest.raises(KeyError):
        create_application([], festivals, participants, 1, 99, TODAY)


def test_cancel_frees_place():
    festivals, participants = make_data(max_places=1)
    applications = []
    create_application(applications, festivals, participants, 1, 1, TODAY)
    assert cancel_application(applications, 1)
    assert applications[0]["status"] == STATUS_CANCELLED
    create_application(applications, festivals, participants, 2, 1, TODAY)
    assert len(applications) == 2


def test_statistics():
    festivals, participants = make_data()
    applications = []
    create_application(applications, festivals, participants, 1, 1, TODAY)
    create_application(applications, festivals, participants, 2, 1, TODAY)
    set_application_status(applications, 1, STATUS_APPROVED)
    assert get_statistics(applications) == {
        STATUS_APPROVED: 1,
        STATUS_SUBMITTED: 1,
    }
