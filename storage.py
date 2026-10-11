"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
from datetime import date
from pathlib import Path


def load_list(filename: Path) -> list[dict]:
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


def save_list(filename: Path, records: list[dict]) -> None:
    """Записать список записей в JSON-файл."""
    Path(filename).parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def load_festivals(filename: Path) -> dict[int, dict]:
    """Загрузить фестивали в словарь {id: данные фестиваля}."""
    festivals = {}
    for record in load_list(filename):
        try:
            festivals[record["id"]] = {
                "id": record["id"],
                "name": record["name"],
                "festival_date": date.fromisoformat(record["festival_date"]),
                "max_places": record["max_places"],
            }
        except (KeyError, ValueError):
            print(f"Пропущена некорректная запись фестиваля: {record}")
    return festivals


def save_festivals(filename: Path, festivals: dict[int, dict]) -> None:
    """Сохранить фестивали в JSON-файл (дата в формате ISO)."""
    records = [
        {**festival, "festival_date": festival["festival_date"].isoformat()}
        for festival in festivals.values()
    ]
    save_list(filename, records)


def load_participants(filename: Path) -> dict[int, dict]:
    """Загрузить участников в словарь {id: данные участника}."""
    participants = {}
    for record in load_list(filename):
        try:
            participants[record["id"]] = {
                "id": record["id"],
                "name": record["name"],
                "email": record["email"],
                "phone": record["phone"],
                "birth_date": date.fromisoformat(record["birth_date"]),
            }
        except (KeyError, ValueError):
            print(f"Пропущена некорректная запись участника: {record}")
    return participants


def save_participants(filename: Path, participants: dict[int, dict]) -> None:
    """Сохранить участников в JSON-файл (дата в формате ISO)."""
    records = [
        {**participant, "birth_date": participant["birth_date"].isoformat()}
        for participant in participants.values()
    ]
    save_list(filename, records)


def load_applications(filename: Path) -> list[dict]:
    """Загрузить список заявок."""
    return load_list(filename)


def save_applications(filename: Path, applications: list[dict]) -> None:
    """Сохранить список заявок."""
    save_list(filename, applications)
