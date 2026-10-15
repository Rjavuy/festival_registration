"""Страницы списка заявок и отдельной заявки."""

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.applications import find_application_by_id, get_statistics
from storage import load_data


def applications(request: HttpRequest) -> HttpResponse:
    """Список заявок из data/applications.json и статистика."""
    _, _, applications_list = load_data(settings.DATA_DIR)
    context = {
        "applications": applications_list,
        "statistics": sorted(get_statistics(applications_list).items()),
    }
    return render(request, "applications/application_list.html", context)


def application_detail(
    request: HttpRequest,
    application_id: int,
) -> HttpResponse:
    """Карточка заявки со связанными объектами; иначе код 404."""
    _, _, applications_list = load_data(settings.DATA_DIR)
    application = find_application_by_id(applications_list, application_id)
    context = {
        "application": application,
    }
    return render(
        request,
        "applications/application_detail.html",
        context,
        status=404 if application is None else 200,
    )
