import csv
import json
import logging
from datetime import datetime

from .errors import IncorrectEventError, IncorrectTimestampError, StreamStatsError
from .models import Event

logger = logging.getLogger(__name__)  # создание логгера для файла

VALID_LEVELS = {
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
}  # Разрешенные имена уровней


def parser_for_csv(file_csv, skip_invalid):
    """
    Принимает на фход file_csv, после с помощью библиотеки csv берёт одну строчку,
    достает из неё данные(timestamp, level, sourse, message) и записывает их в 4 переменные, после происходит валидация.
    """
    reader = csv.DictReader(file_csv)
    for line in reader:  # не использую enumerate т.к, если в файле будет пустая строка то enumerate собъется
        number_line = reader.line_num
        file_time = line.get("timestamp")
        file_level = line.get("level")
        file_source = line.get("source")
        file_message = line.get("message")

        try:
            # Проверка даты
            if not isinstance(file_time, str) or not file_time.strip():
                raise IncorrectTimestampError(f"Строка {number_line}: ошибка в дате")
            try:
                datetime_new = datetime.fromisoformat(
                    file_time
                )  # преобразование из международного времени
            except ValueError:
                raise IncorrectTimestampError(f"Строка {number_line}: ошибка в дате")

            # Проверка уровня
            if not file_level in VALID_LEVELS:
                raise IncorrectEventError(
                    f"Ошибка в строке {number_line}: level не явялется валидным"
                )

            # Проверка источника
            if (
                not isinstance(file_source, str)
                or file_source == None
                or not file_source.strip()
            ):
                raise IncorrectEventError(
                    f"Ошибка в строке {number_line}: не является строкой или является пустой"
                )

            # проверка сообщения
            if not isinstance(file_message, str):
                raise IncorrectEventError(
                    f"Ошибка в строке {number_line}: не является строкой"
                )
            yield Event(
                timestamp=datetime_new,
                level=file_level,
                source=file_source,
                message=file_message,
            )
        except StreamStatsError as err:
            if skip_invalid:
                logger.warning(f"Пропущена строка: {err}")
                yield None
            else:
                raise  # нет err, тк ruff ругался(т.к Python, уже знает,какую ошибку поймал)


def parser_for_json(file_json, skip_invalid):
    """
    Принимает на фход file_json, берёт одну строчку
    достает из неё данные(timestamp, level, sourse, message) и записывает их в 4 переменные, после происходит валидация.
    """
    for number_line, line in enumerate(file_json, start=1):
        if not line.strip():
            continue  # т.к в файле json в конце может быть пустая строчка(/n)
        try:
            try:
                line_str = json.loads(line)
                file_time = line_str.get("timestamp")
                file_level = line_str.get("level")
                file_source = line_str.get("source")
                file_message = line_str.get("message")
            except json.JSONDecodeError:  # строка не является корректным JSON
                raise IncorrectEventError(f"Ошибка в строке {number_line}")

            if not isinstance(file_time, str) or not file_time.strip():
                raise IncorrectTimestampError(f"Строка {number_line}: ошибка в дате")
            try:
                datetime_new = datetime.fromisoformat(
                    file_time
                )  # преобразование из международного времени
            except ValueError:
                raise IncorrectTimestampError(f"Строка {number_line}: ошибка в дате")

            # Проверка уровня
            if not file_level in VALID_LEVELS:
                raise IncorrectEventError(
                    f"Ошибка в строке {number_line}: level не явялется валидным"
                )
            # Проверка источника
            if (
                not isinstance(file_source, str)
                or file_source == None
                or not file_source.strip()
            ):
                raise IncorrectEventError(
                    f"Ошибка в строке {number_line}: не является строкой или является пустой"
                )

            # проверка сообщения
            if not isinstance(file_message, str):
                raise IncorrectEventError(
                    f"Ошибка в строке {number_line}: не является строкой"
                )

            yield Event(
                timestamp=datetime_new,
                level=file_level,
                source=file_source,
                message=file_message,
            )
        except StreamStatsError as err:
            if skip_invalid:
                logger.warning(f"Пропущена строка: {err}") #кидается в ошибки логгера
                yield None
            else:
                raise  # нет err, тк ruff ругался(т.к Python, уже знает,какую ошибку поймал)
