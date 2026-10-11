import json
from datetime import date

from models import Application, Festival, Participant
from storage import (
    load_applications,
    load_festivals,
    load_list,
    save_applications,
    save_festivals,
)


def test_save_and_load_festivals(tmp_path):
    filename = tmp_path / "festivals.json"
    save_festivals(filename, [
        Festival(1, "Фестиваль искусств", date(2026, 12, 15), 100),
    ])
    festival = load_festivals(filename)[0]
    assert isinstance(festival, Festival)
    assert festival.festival_date == date(2026, 12, 15)


def test_applications_restore_links(tmp_path):
    filename = tmp_path / "applications.json"
    festival = Festival(1, "Фестиваль", date(2026, 12, 15), 10)
    ivan = Participant(1, "Иван", "ivan@example.com", "+79161234567",
                       date(2000, 5, 15))
    application = Application(1, festival, ivan)
    application.approve()
    save_applications(filename, [application])

    saved = json.loads(filename.read_text(encoding="utf-8"))
    assert saved[0]["festival_id"] == 1
    assert saved[0]["participant_id"] == 1

    loaded = load_applications(filename, [festival], [ivan])[0]
    assert loaded.festival is festival
    assert loaded.participant is ivan
    assert loaded.status == application.status


def test_application_with_unknown_festival_skipped(tmp_path):
    filename = tmp_path / "applications.json"
    filename.write_text(json.dumps([{
        "id": 1, "festival_id": 5, "participant_id": 1,
        "status": "Отправлена",
    }]), encoding="utf-8")
    assert load_applications(filename, [], []) == []


def test_load_missing_file(tmp_path):
    assert load_list(tmp_path / "missing.json") == []


def test_load_broken_file(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("{ not json", encoding="utf-8")
    assert load_list(filename) == []
