import json

from .models import Stats


def sort_for_sorted(item):
    """
    Сортирует кортеж по количеству ошибок(от большего к меньшему)
    При равном кол-ве ошибок ставит вперед тот кортеж, в котором буква идет раньше по алфавиту.
    """
    name = item[0]
    inf = item[1]
    return (-inf["errors"], name)


def report_json(stats: Stats, to_go: str) -> None:
    sorted_soerces = sorted(
        stats.sources.items(), key=sort_for_sorted
    )  # list переделывает словарь в список пар
    top_5_err = []
    for name, info in sorted_soerces[:5]:
        top_5_err.append({"source": name, "errors": info["errors"]})
    data = {}  # хранит переменные для переноса их в json

    # Иморт данных из Stats и их экспорт  в data
    data["total"] = stats.total
    data["levels"] = dict(
        stats.levels
    )  # нужно обернуть в словарь, тк Json не принимает Counter
    data["sources"] = stats.sources
    data["skipped_invalid"] = stats.skipped_invalid

    data["top_errors"] = top_5_err

    # Импорт и проверка времени на валидность
    first_time = stats.first_timestamp
    last_time = stats.last_timestamp

    # Провека первой даты
    if first_time is None:  # в первой дате лежит None
        pass

    else:
        first_time = first_time.isoformat()

    # Экспорт в data
    data["first_timestamp"] = first_time

    # Проверка конечной даты
    if last_time is None:
        pass

    else:
        last_time = last_time.isoformat()

    # Экспорт в data
    data["last_timestamp"] = last_time

    # Запись в файл
    with open(to_go, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
