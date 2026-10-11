"""Страницы списка фестивалей и отдельного фестиваля."""

from datetime import date

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.applications import count_taken_places
from models.festivals import find_festival_by_id, sort_festivals
from storage import load_data
from utils import DATE_FORMAT


def festivals(request: HttpRequest) -> HttpResponse:
    """Список фестивалей из data/festivals.json."""
    festivals_list, _, applications = load_data(settings.DATA_DIR)
    today = date.today()
    items = ""
    for festival in sort_festivals(festivals_list):
        free = festival.max_places - count_taken_places(
            applications, festival
        )
        if not festival.is_registration_open(today):
            badge, status = "bg-secondary", "завершён"
        elif free <= 0:
            badge, status = "bg-danger", "мест нет"
        else:
            badge, status = "bg-success", "приём заявок"
        items += f"""
        <a href="/festivals/{festival.id}/"
           class="list-group-item list-group-item-action
                  d-flex justify-content-between align-items-center">
            <span>
                {escape(festival.name)}
                <small class="text-muted">
                    – {festival.festival_date.strftime(DATE_FORMAT)},
                    свободно {free} из {festival.max_places}
                </small>
            </span>
            <span class="badge {badge}">{status}</span>
        </a>"""
    content = f"""
    <h1 class="mb-3">Фестивали</h1>
    <div class="list-group">{items}</div>
    """
    return HttpResponse(page("Фестивали", content))


def festival_detail(request: HttpRequest, festival_id: int) -> HttpResponse:
    """Карточка фестиваля; если фестиваль не найден – код 404."""
    festivals_list, _, applications = load_data(settings.DATA_DIR)
    festival = find_festival_by_id(festivals_list, festival_id)
    if festival is None:
        content = """
        <h1 class="text-danger">Фестиваль не найден</h1>
        <a href="/festivals/" class="btn btn-outline-secondary">
            ← к списку фестивалей
        </a>
        """
        return HttpResponse(page("Фестиваль не найден", content), status=404)

    taken = count_taken_places(applications, festival)
    can_apply = (
        festival.is_registration_open(date.today())
        and festival.has_free_places(taken)
    )
    badge = "bg-success" if can_apply else "bg-danger"
    status = "можно подать заявку" if can_apply else "приём заявок закрыт"
    rows = "".join(
        f"""<li class="list-group-item">
            <a href="/applications/{a.id}/">
                {escape(a.participant.name)}</a> – {a.status}
        </li>"""
        for a in applications if a.festival.id == festival.id
    ) or '<li class="list-group-item text-muted">Заявок нет</li>'
    content = f"""
    <div class="card mb-3">
        <div class="card-body">
            <h2 class="card-title">{escape(festival.name)}</h2>
            <p class="card-text"><strong>Дата проведения:</strong>
                {festival.festival_date.strftime(DATE_FORMAT)}</p>
            <p class="card-text"><strong>Мест:</strong>
                {festival.max_places}, занято {taken}</p>
            <p class="card-text">Статус на сегодня:
                <span class="badge {badge}">{status}</span></p>
        </div>
    </div>
    <h3 class="h5">Заявки на фестиваль</h3>
    <ul class="list-group mb-3">{rows}</ul>
    <a href="/festivals/" class="btn btn-outline-secondary">
        ← к списку фестивалей
    </a>
    """
    return HttpResponse(page(escape(festival.name), content))
