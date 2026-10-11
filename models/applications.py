"""Класс Application и функции подачи и обработки заявок."""

from datetime import date
from typing import Callable, Dict, List, Optional

from utils import next_id
from validators import MIN_AGE

from .festivals import Festival
from .participants import Participant

STATUS_SUBMITTED = "Отправлена"
STATUS_APPROVED = "Одобрена"
STATUS_REJECTED = "Отклонена"
STATUS_CANCELLED = "Отменена"

# Заявки с этими статусами занимают место на фестивале.
ACTIVE_STATUSES = {STATUS_SUBMITTED, STATUS_APPROVED}
ALL_STATUSES = ACTIVE_STATUSES | {STATUS_REJECTED, STATUS_CANCELLED}


class Application:
    """Заявка участника на фестиваль.

    Статус хранится в закрытом атрибуте и меняется только методами
    approve(), reject() и cancel().
    """

    def __init__(
        self,
        application_id: int,
        festival: Festival,
        participant: Participant,
        status: str = STATUS_SUBMITTED,
    ) -> None:
        """Создать заявку, связанную с фестивалем и участником."""
        if status not in ALL_STATUSES:
            raise ValueError(f"Неизвестный статус заявки: {status}")
        self.id = application_id
        self.festival = festival
        self.participant = participant
        self._status = status

    @property
    def status(self) -> str:
        """Текущий статус заявки (только чтение)."""
        return self._status

    @property
    def is_active(self) -> bool:
        """Заявка занимает место на фестивале."""
        return self._status in ACTIVE_STATUSES

    def _change_status(self, new_status: str) -> None:
        """Сменить статус активной заявки."""
        if not self.is_active:
            raise ValueError(f"Заявка уже имеет статус «{self._status}»")
        self._status = new_status

    def approve(self) -> None:
        """Одобрить заявку (решение организатора)."""
        self._change_status(STATUS_APPROVED)

    def reject(self) -> None:
        """Отклонить заявку (решение организатора)."""
        self._change_status(STATUS_REJECTED)

    def cancel(self) -> None:
        """Отменить заявку: объект остаётся в коллекции."""
        self._change_status(STATUS_CANCELLED)

    def __str__(self) -> str:
        """Вернуть строковое представление заявки."""
        return (
            f"Заявка №{self.id}: {self.participant.name} -> "
            f"{self.festival.name} [{self._status}]"
        )


def check_application_possibility(
    age: int,
    festival_date: date,
    current_date: date,
    max_places: int,
    taken_places: int,
) -> str:
    """Проверить, может ли участник подать заявку (функция из ПР1)."""
    if age < MIN_AGE:
        return "Отклонена: возраст меньше 14 лет"
    if current_date > festival_date:
        return "Отклонена: дедлайн подачи заявок прошёл"
    if taken_places >= max_places:
        return "Отклонена: свободных мест нет"
    return STATUS_SUBMITTED


def count_taken_places(
    applications: List[Application],
    festival: Festival,
) -> int:
    """Посчитать места, занятые активными заявками на фестиваль."""
    return sum(
        1 for a in applications if a.festival.id == festival.id and a.is_active
    )


def has_active_application(
    applications: List[Application],
    participant: Participant,
    festival: Festival,
) -> bool:
    """Проверить, есть ли у участника активная заявка на фестиваль."""
    return any(
        a.participant.id == participant.id
        and a.festival.id == festival.id
        and a.is_active
        for a in applications
    )


def create_application(
    applications: List[Application],
    festival: Festival,
    participant: Participant,
    current_date: date,
) -> Application:
    """Проверить возможность участия, создать заявку и добавить в коллекцию.

    Если подать заявку нельзя, возбуждается ValueError с причиной.
    """
    if has_active_application(applications, participant, festival):
        raise ValueError("Участник уже подал заявку на этот фестиваль")
    status = check_application_possibility(
        participant.age_on(current_date),
        festival.festival_date,
        current_date,
        festival.max_places,
        count_taken_places(applications, festival),
    )
    if status != STATUS_SUBMITTED:
        raise ValueError(status)
    application = Application(
        next_id(a.id for a in applications), festival, participant
    )
    applications.append(application)
    return application


def find_application_by_id(
    applications: List[Application],
    application_id: int,
) -> Optional[Application]:
    """Найти заявку по идентификатору."""
    for application in applications:
        if application.id == application_id:
            return application
    return None


def change_application_status(
    applications: List[Application],
    application_id: int,
    action: Callable[[Application], None],
) -> bool:
    """Найти заявку и применить к ней метод action.

    action – метод класса: Application.approve, Application.reject
    или Application.cancel. Возвращает True, если статус изменён.
    """
    application = find_application_by_id(applications, application_id)
    if application is None:
        return False
    try:
        action(application)
    except ValueError:
        return False
    return True


def cancel_application(
    applications: List[Application],
    application_id: int,
) -> bool:
    """Отменить заявку по идентификатору."""
    return change_application_status(
        applications, application_id, Application.cancel
    )


def get_statistics(applications: List[Application]) -> Dict[str, int]:
    """Посчитать количество заявок по каждому статусу."""
    statistics: Dict[str, int] = {}
    for application in applications:
        statistics[application.status] = (
            statistics.get(application.status, 0) + 1
        )
    return statistics
