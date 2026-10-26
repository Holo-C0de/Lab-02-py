from .models import Event, Stats


def update_stats(stats: Stats, event: Event) -> None:
    stats.total += 1  # увеличение всех событий на 1
    stats.levels[event.level] += 1  # Создание нового ключа(если такого не было)
    # и увеличение счетчика на 1

    # словарь есть
    if event.source in stats.sources:  # {"total": 0, "errors": 0}
        stats.sources[event.source]["total"] += (
            1  # увеличение total в словаре источника
        )

    else:  # словаря нет -> создаём новый словарь
        stats.sources[event.source] = {"total": 1, "errors": 0}

        # проверка(является ли собитие ошибочным)
    if event.level in ("ERROR", "CRITICAL"):
        stats.sources[event.source]["errors"] += 1

    if stats.first_timestamp is None or event.timestamp < stats.first_timestamp:
        stats.first_timestamp = event.timestamp

    if stats.last_timestamp is None or event.timestamp > stats.last_timestamp:
        stats.last_timestamp = event.timestamp
