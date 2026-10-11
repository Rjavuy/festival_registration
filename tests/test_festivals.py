from datetime import date

import pytest

from models import Festival
from models.festivals import (
    add_festival,
    filter_upcoming_festivals,
    find_festival_by_id,
    find_festivals,
    sort_festivals,
)


def make_festivals():
    festivals = []
    add_festival(festivals, "Зимний джаз", date(2027, 2, 20), 50)
    add_festival(festivals, "Фестиваль искусств", date(2026, 12, 15), 100)
    add_festival(festivals, "Летний рок", date(2026, 8, 1), 200)
    return festivals


def test_festival_creation():
    festival = Festival(1, "Фестиваль искусств", date(2026, 12, 15), 100)
    assert festival.id == 1
    assert festival.name == "Фестиваль искусств"
    assert festival.max_places == 100
    assert str(festival) == "Фестиваль искусств (15.12.2026, мест: 100)"


def test_festival_invalid_places():
    assert not Festival.validate_max_places(0)
    with pytest.raises(ValueError):
        Festival(1, "Пустой", date(2027, 1, 1), 0)


def test_festival_registration_open():
    festival = Festival(1, "Фестиваль", date(2026, 12, 15), 2)
    assert festival.is_registration_open(date(2026, 12, 15))
    assert not festival.is_registration_open(date(2026, 12, 16))
    assert festival.has_free_places(1)
    assert not festival.has_free_places(2)


def test_add_festival():
    festivals = make_festivals()
    assert len(festivals) == 3
    assert isinstance(festivals[0], Festival)
    assert find_festival_by_id(festivals, 2).name == "Фестиваль искусств"
    assert find_festival_by_id(festivals, 99) is None


def test_find_festivals():
    found = find_festivals(make_festivals(), "ДЖАЗ")
    assert [f.id for f in found] == [1]


def test_filter_upcoming_festivals():
    upcoming = filter_upcoming_festivals(make_festivals(), date(2026, 10, 1))
    assert {f.id for f in upcoming} == {1, 2}


def test_sort_festivals():
    festivals = make_festivals()
    assert [f.id for f in sort_festivals(festivals)] == [3, 2, 1]
    assert [f.id for f in sort_festivals(festivals, by="name")] == [1, 3, 2]
