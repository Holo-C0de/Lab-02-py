import io  # для создания фейковых файлов в памяти
from datetime import datetime

import pytest
from streamstats.analysis import update_stats
from streamstats.errors import IncorrectTimestampError, IncorrectEventError
from streamstats.models import Event, Stats
from streamstats.parsers import parser_for_csv, parser_for_json


# Исправный файл csv
def test_csv_valid():
    fake_file = io.StringIO(
        'timestamp,level,source,message\n2026-10-06T10:00:00+00:00,INFO,api,"Ку, тестовый тест"'
    )

    # запуск парсера
    events = list(parser_for_csv(fake_file, skip_invalid=False))
    # нужен list, чтобы получить список собыйтий
    assert len(events) == 1  # должно быть одно событие
    assert events[0].level == "INFO"
    assert events[0].message == "Ку, тестовый тест"


# Исправный файл json
def test_jsonl_valid():
    fake_file = io.StringIO(
        '{"timestamp": "2026-10-06T10:00:00+00:00", "level": "INFO", "source": "api", "message": "Ку, тестовый тест"}'
    )
    events = list(parser_for_json(fake_file, skip_invalid=False))
    assert len(events) == 1
    assert events[0].level == "INFO"
    assert events[0].message == "Ку, тестовый тест"


# Файл с неверной строкой
def test_csv_invalid_data():  # Проверка (неверная дата)
    fake_file = io.StringIO("timestamp,level,source,message\nnot-a-date,INFO,api,тест")
    with pytest.raises(IncorrectTimestampError):
        list(parser_for_csv(fake_file, skip_invalid=False))


# Пустой файл-------
def test_empty_file_csv():
    fake_file = io.StringIO("")
    events = list(parser_for_csv(fake_file, skip_invalid=False))
    assert len(events) == 0


def test_empty_file_json():
    fake_file = io.StringIO("Теееееекст")
    with pytest.raises(IncorrectEventError):
        list(parser_for_json(fake_file, skip_invalid=False))


# Пустой файл-------
# --skip-invalid (файл с битой строкой)
def test_skip_inval():
    fake_file = io.StringIO("timestamp,level,source,message\nnot-a-date,INFO,api,Тест")
    events = list(parser_for_csv(fake_file, skip_invalid=True))
    assert events[0] is None


# Тест передача нескольких файлов
def test_many_files():
    stats = Stats()
    event1 = Event(
        timestamp=datetime.fromisoformat("2026-10-06T10:00:00+00:00"),
        level="INFO",
        source="api",
        message="Первое",
    )
    event2 = Event(
        timestamp=datetime.fromisoformat("2026-10-06T11:00:00+00:00"),
        level="ERROR",
        source="db",
        message="Второе",
    )

    update_stats(stats, event1)
    update_stats(stats, event2)

    assert stats.total == 2  # всего 2 события
    assert stats.levels["INFO"] == 1  # один INFO
    assert stats.levels["ERROR"] == 1  # один ERROR

    assert stats.sources["api"]["total"] == 1
    assert stats.sources["db"]["total"] == 1
    assert stats.sources["db"]["errors"] == 1
    assert stats.first_timestamp == event1.timestamp
    assert stats.last_timestamp == event2.timestamp
