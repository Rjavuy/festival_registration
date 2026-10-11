from datetime import date

import pytest

from festivals import (
    add_festival,
    filter_upcoming_festivals,
    find_festivals,
    sort_festivals,
)


def make_festivals():
    festivals = {}
    add_festival(festivals, "Зимний джаз", date(2027, 2, 20), 50)
    add_festival(festivals, "Фестиваль искусств", date(2026, 12, 15), 100)
    add_festival(festivals, "Летний рок", date(2026, 8, 1), 200)
    return festivals


def test_add_festival():
    festivals = make_festivals()
    assert len(festivals) == 3
    assert festivals[1]["name"] == "Зимний джаз"


def test_add_festival_without_places():
    with pytest.raises(ValueError):
        add_festival({}, "Пустой", date(2027, 1, 1), 0)


def test_find_festivals():
    found = find_festivals(make_festivals(), "ДЖАЗ")
    assert [f["id"] for f in found] == [1]


def test_filter_upcoming_festivals():
    upcoming = filter_upcoming_festivals(make_festivals(), date(2026, 10, 1))
    assert {f["id"] for f in upcoming} == {1, 2}


def test_sort_festivals_by_date():
    ordered = sort_festivals(make_festivals())
    assert [f["id"] for f in ordered] == [3, 2, 1]
