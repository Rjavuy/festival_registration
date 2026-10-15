"""Страницы списка фестивалей и отдельного фестиваля."""

from datetime import date

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.applications import count_taken_places
from models.festivals import find_festival_by_id, sort_festivals
from storage import load_data


def festivals(request: HttpRequest) -> HttpResponse:
    """Список фестивалей из data/festivals.json."""
    festivals_list, _, applications = load_data(settings.DATA_DIR)
    today = date.today()
    items = []
    for festival in sort_festivals(festivals_list):
        taken = count_taken_places(applications, festival)
        items.append({
            "festival": festival,
            "free": festival.max_places - taken,
            "is_open": festival.is_registration_open(today),
            "has_places": festival.has_free_places(taken),
        })
    context = {
        "items": items,
    }
    return render(request, "festivals/festival_list.html", context)


def festival_detail(request: HttpRequest, festival_id: int) -> HttpResponse:
    """Карточка фестиваля; если фестиваль не найден – код 404."""
    festivals_list, _, applications = load_data(settings.DATA_DIR)
    festival = find_festival_by_id(festivals_list, festival_id)
    context = {
        "festival": festival,
    }
    if festival is not None:
        taken = count_taken_places(applications, festival)
        context.update({
            "taken": taken,
            "can_apply": (
                festival.is_registration_open(date.today())
                and festival.has_free_places(taken)
            ),
            "festival_applications": [
                a for a in applications if a.festival.id == festival.id
            ],
        })
    return render(
        request,
        "festivals/festival_detail.html",
        context,
        status=404 if festival is None else 200,
    )
