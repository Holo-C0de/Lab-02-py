import argparse
import logging  # Нужен для логов
import sys

from .analysis import update_stats
from .errors import StreamStatsError
from .models import Stats
from .parsers import parser_for_csv, parser_for_json
from .report import report_json


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Потоковый анализатор логов",
        epilog="""
    Примеры использования:
    python -m streamstats analyze data.csv --format csv --output report.json
    python -m streamstats analyze file1.csv file2.csv --format csv --output total.json
    python -m streamstats analyze data.csv --format csv --skip-invalid --output report.json
    """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze_parser = subparsers.add_parser("analyze", help="Анализ логов")

    # Блок команд -------
    analyze_parser.add_argument(
        "inputs", nargs="+", help="Пути к входным файлам"
    )  # путь к файлу, который нужно прочитать
    # nargs="+" - позволяет ввести больше одного адреса => может быть несколько форматов

    # формат файла
    analyze_parser.add_argument(
        "--format", choices=["csv", "jsonl"], required=True, help="Формат файлов"
    )  # required=True - запуск без информации о типе файла

    # Адрес файла, в который нужно записать данные
    analyze_parser.add_argument("--output", required=True, help="Путь к файлу отчета")

    # Режим пропуска ошибок
    analyze_parser.add_argument(
        "--skip-invalid", action="store_true", help="Пропуск битых строк"
    )
    # Блок комманд -------

    args = parser.parse_args()  # чтение команды из консоли(сама команда)

    stats = Stats()

    logging.basicConfig(level=logging.WARNING, format="%(message)s")

    # Словарь парсеров
    need_parser = {"csv": parser_for_csv, "jsonl": parser_for_json}

    cur_parser = need_parser[args.format]  # по ключу находим нужный парсер

    for fileadress in args.inputs:  # проходим по всем введенным адресам
        with open(fileadress, "r", encoding="utf-8") as file:
            try:
                for item in cur_parser(file, args.skip_invalid):
                    if item is None:
                        stats.skipped_invalid += 1

                    else:
                        update_stats(stats, item)
            except StreamStatsError as err:
                print(f"Ошибка в файле {fileadress}: {err}", file=sys.stderr)
                sys.exit(2)

    to_go = args.output
    report_json(stats, to_go)


if __name__ == "__main__":
    main()
