from datetime import datetime

from streamstats.analysis import update_stats
from streamstats.models import Event, Stats


def test_stats_aggregation():
    stats = Stats()  # фальшивая пустая статистика

    event1 = Event(
        timestamp=datetime.fromisoformat("2026-10-06T10:00:00+00:00"),
        level="INFO",
        source="api",
        message="Первое сообщение",
    )
    event2 = Event(
        timestamp=datetime.fromisoformat("2026-10-06T11:00:00+00:00"),
        level="ERROR",
        source="db",
        message="Второе сообщение",
    )
    # Экспорт в анализатор
    update_stats(stats, event1)
    update_stats(stats, event2)

    # Сохраниловсь точно две статистки
    assert stats.total == 2

    assert stats.levels["INFO"] == 1
    assert stats.levels["ERROR"] == 1
    assert stats.sources["api"]["total"] == 1
    assert stats.sources["api"]["errors"] == 0
    assert stats.sources["db"]["total"] == 1
    assert stats.sources["db"]["errors"] == 1

    # Проверка определения дат
    assert stats.first_timestamp == event1.timestampс
    assert stats.last_timestamp == event2.timestamp
