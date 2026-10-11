"""Главная страница, общий каркас страниц и обработчик ошибки 404."""

from django.http import HttpRequest, HttpResponse

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def page(title: str, content: str) -> str:
    """Собрать HTML-документ: Bootstrap, навигация и содержимое."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand bg-primary mb-4" data-bs-theme="dark">
        <div class="container">
            <a class="navbar-brand" href="/">Фестивали</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/festivals/">Фестивали</a>
                <a class="nav-link" href="/applications/">Заявки</a>
            </div>
        </div>
    </nav>
    <main class="container pb-4">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание приложения и навигация."""
    content = """
    <h1 class="display-5">Регистрация участников фестиваля</h1>
    <p class="lead">
        Приложение для подачи и обработки заявок на участие в фестивалях.
    </p>
    <p>
        Участники подают заявки, организаторы проверяют их и присваивают
        статус. Заявку можно подать, если участнику не меньше 14 лет,
        фестиваль ещё не прошёл и остались свободные места.
    </p>
    <a href="/festivals/" class="btn btn-primary me-2">Фестивали</a>
    <a href="/applications/" class="btn btn-secondary">Заявки</a>
    """
    return HttpResponse(page("Регистрация на фестивали", content))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Собственная страница ошибки 404."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
