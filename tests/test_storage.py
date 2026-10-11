from datetime import date

from festivals import add_festival
from storage import load_festivals, load_list, save_festivals


def test_save_and_load_festivals(tmp_path):
    filename = tmp_path / "festivals.json"
    festivals = {}
    add_festival(festivals, "Фестиваль искусств", date(2026, 12, 15), 100)
    save_festivals(filename, festivals)
    assert load_festivals(filename) == festivals


def test_load_missing_file(tmp_path):
    assert load_list(tmp_path / "missing.json") == []


def test_load_broken_file(tmp_path):
    filename = tmp_path / "broken.json"
    filename.write_text("{ not json", encoding="utf-8")
    assert load_list(filename) == []
