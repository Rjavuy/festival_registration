"""Сохранение и загрузка данных: преобразование JSON <-> объекты."""

import json
from datetime import date
from pathlib import Path
from typing import List

from models import Application, Festival, Participant
from models.festivals import find_festival_by_id
from models.participants import find_participant_by_id


def load_list(filename: Path) -> List[dict]:
    """Прочитать список записей из JSON-файла.

    Если файла нет или он повреждён, возвращается пустой список.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, будет создан новый.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные не загружены.")
        return []
    if not isinstance(data, list):
        print(f"Файл {filename} имеет неверный формат.")
        return []
    return data


def save_list(filename: Path, records: List[dict]) -> None:
    """Записать список записей в JSON-файл."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)
        file.write("\n")


def load_festivals(filename: Path) -> List[Festival]:
    """Загрузить фестивали: JSON -> объекты Festival."""
    festivals = []
    for record in load_list(filename):
        try:
            festivals.append(Festival(
                festival_id=record["id"],
                name=record["name"],
                festival_date=date.fromisoformat(record["festival_date"]),
                max_places=record["max_places"],
            ))
        except (KeyError, ValueError):
            print(f"Пропущена некорректная запись фестиваля: {record}")
    return festivals


def save_festivals(filename: Path, festivals: List[Festival]) -> None:
    """Сохранить фестивали: объекты Festival -> JSON."""
    save_list(filename, [
        {
            "id": festival.id,
            "name": festival.name,
            "festival_date": festival.festival_date.isoformat(),
            "max_places": festival.max_places,
        }
        for festival in festivals
    ])


def load_participants(filename: Path) -> List[Participant]:
    """Загрузить участников: JSON -> объекты Participant."""
    participants = []
    for record in load_list(filename):
        try:
            participants.append(Participant.from_data(record))
        except (KeyError, ValueError):
            print(f"Пропущена некорректная запись участника: {record}")
    return participants


def save_participants(
    filename: Path,
    participants: List[Participant],
) -> None:
    """Сохранить участников: объекты Participant -> JSON."""
    save_list(filename, [
        {
            "id": participant.id,
            "name": participant.name,
            "email": participant.email,
            "phone": participant.phone,
            "birth_date": participant.birth_date.isoformat(),
        }
        for participant in participants
    ])


def load_applications(
    filename: Path,
    festivals: List[Festival],
    participants: List[Participant],
) -> List[Application]:
    """Загрузить заявки и восстановить связи с фестивалем и участником.

    Заявки, ссылающиеся на несуществующие объекты, пропускаются.
    """
    applications = []
    for record in load_list(filename):
        try:
            festival = find_festival_by_id(festivals, record["festival_id"])
            participant = find_participant_by_id(
                participants, record["participant_id"]
            )
            if festival is None or participant is None:
                raise ValueError("связанный объект не найден")
            applications.append(Application(
                application_id=record["id"],
                festival=festival,
                participant=participant,
                status=record["status"],
            ))
        except (KeyError, ValueError):
            print(f"Пропущена некорректная запись заявки: {record}")
    return applications


def save_applications(
    filename: Path,
    applications: List[Application],
) -> None:
    """Сохранить заявки: ссылки на объекты заменяются идентификаторами."""
    save_list(filename, [
        {
            "id": application.id,
            "festival_id": application.festival.id,
            "participant_id": application.participant.id,
            "status": application.status,
        }
        for application in applications
    ])
