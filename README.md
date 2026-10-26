# Лабораторная работа 2: Потоковый анализатор логов

Программа на Python для чтения логов из файлов форматов CSV и JSONL, подсчета статистики и сохранения отчета в JSON.


## Особенности:

### Потоковое чтение:

Парсеры используют генераторы (```yield```), поэтому файлы читаются строго построчно. Это экономит память и позволяет обрабатывать большие файлы.

### Словарь парсеров:

В ```__main__.py``` выбор парсера происходит через словарь ```need_parser = {"csv": parser_for_csv, "jsonl": parser_for_json}```. Это позволяет легко добавлять новые форматы без изменения основной логики.

### Статистика:

Считаются уровни, источники, Top-5 источников ошибок (сортировка по убыванию ошибок и по алфавиту при равенстве).

## Структура проекта:

* src/streamstats/models.py — модели данных (Event и Stats).

* src/streamstats/parsers.py — чтение и валидация CSV/JSONL.

* src/streamstats/analysis.py — обновление статистики.

* src/streamstats/report.py — сохранение отчета и сортировка Top-5.

* src/streamstats/__main__.py — CLI-интерфейс (парсинг аргументов).

* tests/ — тесты парсеров и интеграционный тест CLI.

## Скачивание
Для установки пакета выполните команду в корневой папке проекта:
```bash
git clone https://github.com/Holo-C0de/https://github.com/Holo-C0de/Lab-02-py.git
cd Lab-02-py
```
```bash
pip install -e .
```
## Запуск(команды)
```bash
python -m streamstats analyze <файлы> --format <csv|jsonl> --output <имя_отчета.json>
```
### Запуск с одним файлом:
```bash
python -m streamstats analyze data/events_valid.csv --format csv --output report.json
```
### Запуск с N файлами:
```bash
python -m streamstats analyze data/file1.csv data/file2.csv --format csv --output total_report.json
```
### Обработка ошибок (флаг --skip-invalid)
```bash
python -m streamstats analyze data/events_invalid.csv --format csv --skip-invalid --output report_invalid.json
```
## Проверка кода и тесты

### Запуск тестов
```bash
pytest
```
### Проверка на pep-8
```bash
ruff check .
```
