class StreamStatsError(Exception):
    """Базовая ошибка пакета."""


class UnsupportedFormatError(StreamStatsError):
    """Неподдерживаемый формат."""


class CliConfigError(StreamStatsError):
    """Ошибка конфигурации CLI."""


class IncorrectEventError(StreamStatsError):
    """Неверное событие."""


class IncorrectTimestampError(IncorrectEventError):
    """Неверное время."""
