"""Страницы списка заявок и отдельной заявки."""

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page
from models import Application
from models.applications import (
    STATUS_APPROVED,
    STATUS_SUBMITTED,
    find_application_by_id,
    get_statistics,
)
from storage import load_data
from utils import DATE_FORMAT

STATUS_BADGES = {
    STATUS_SUBMITTED: "bg-primary",
    STATUS_APPROVED: "bg-success",
}


def status_badge(application: Application) -> str:
    """Вернуть HTML-бейдж со статусом заявки."""
    css = STATUS_BADGES.get(application.status, "bg-secondary")
    return f'<span class="badge {css}">{application.status}</span>'


def applications(request: HttpRequest) -> HttpResponse:
    """Список заявок из data/applications.json и статистика."""
    _, _, applications_list = load_data(settings.DATA_DIR)
    items = ""
    for application in applications_list:
        items += f"""
        <a href="/applications/{application.id}/"
           class="list-group-item list-group-item-action
                  d-flex justify-content-between align-items-center">
            <span>№{application.id}.
                {escape(application.participant.name)} –
                {escape(application.festival.name)}</span>
            {status_badge(application)}
        </a>"""
    statistics = ", ".join(
        f"{status}: {count}"
        for status, count in sorted(get_statistics(applications_list).items())
    )
    content = f"""
    <h1 class="mb-3">Заявки</h1>
    <p class="text-muted">Всего: {len(applications_list)}.
        {statistics}</p>
    <div class="list-group">{items}</div>
    """
    return HttpResponse(page("Заявки", content))


def application_detail(
    request: HttpRequest,
    application_id: int,
) -> HttpResponse:
    """Карточка заявки со связанными объектами; иначе код 404."""
    _, _, applications_list = load_data(settings.DATA_DIR)
    application = find_application_by_id(applications_list, application_id)
    if application is None:
        content = """
        <h1 class="text-danger">Заявка не найдена</h1>
        <a href="/applications/" class="btn btn-outline-secondary">
            ← к списку заявок
        </a>
        """
        return HttpResponse(page("Заявка не найдена", content), status=404)

    festival = application.festival
    participant = application.participant
    content = f"""
    <div class="card">
        <div class="card-body">
            <h2 class="card-title">Заявка №{application.id}</h2>
            <p class="card-text"><strong>Фестиваль:</strong>
                <a href="/festivals/{festival.id}/">
                    {escape(festival.name)}</a>,
                {festival.festival_date.strftime(DATE_FORMAT)}</p>
            <p class="card-text"><strong>Участник:</strong>
                {escape(participant.name)},
                {escape(participant.email)}</p>
            <p class="card-text"><strong>Статус:</strong>
                {status_badge(application)}</p>
            <a href="/applications/" class="btn btn-outline-secondary">
                ← к списку заявок
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(f"Заявка №{application.id}", content))
