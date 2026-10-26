from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True, slots=True)  # frozen=True - защита от перезаписи
# slots=True - отключает создние скрытого словаря, позволяет экономить место
class Event:  # этот класс для чтения файлов
    timestamp: datetime  # время
    level: str  # уровень
    source: str  # источник сообщения
    message: str  # само сообщение


@dataclass
class Stats:  # это класс хранит статистику
    total: int = 0  # счетчик(считает все правильные строки(Без заголовка в csv файле))
    skipped_invalid: int = 0  # Счетчик кол-ва пропущенных плохих строк(без заголовка csv) со включенным режимом --skip-invalid
    levels: Counter = field(
        default_factory=Counter  # key - str, value - int, default_factory=Counter - создавать каждый раз новый
    )  # словарь для подсчетов для нового Stats
    # Counter - автоматически создает новый ключ и ставит значение 0, если такого ключа не было
    sources: dict[str, dict[str, int]] = field(
        default_factory=dict
    )  # необходим словарь в словаре для тз(подсчет топ 5 источников по ошибкам)
    # в первой части словаря имя источника(source), во 2 части по первому ключу - все события, по 2 ключу кол-во ошибок
    first_timestamp: datetime | None = None
    last_timestamp: datetime | None = (
        None  # datetime | None - такая запись необходима, для устранения ошибки
    )

    # т.к @dataclass работает только с аннотациями типов(явное указание типа), поэтому нужно ставить :
