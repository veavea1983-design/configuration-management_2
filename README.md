# Анализатор зависимостей Ubuntu apt

Практическая работа №2 по дисциплине
«Конфигурационное управление».

Вариант №3. Язык реализации: Python 3.

## Назначение

Программа предназначена для анализа зависимостей
пакетов Ubuntu и их визуализации.

## Этап 1. Конфигурация

Реализовано чтение настроек из INI-файла,
проверка параметров и вывод ключ-значение.

## Настройки

- `package` — имя анализируемого пакета.
- `repository` — URL репозитория или путь к файлу.
- `test_mode` — режим тестового репозитория.
- `version` — версия пакета.
- `output` — имя выходного PNG-файла.

## Структура проекта

- `src/config.py` — чтение и проверка INI.
- `src/main.py` — запуск приложения.
- `tests/test_project.py` — автоматические тесты.
- `config.ini` — настройки.
- `run.bat` — запуск на Windows.

## Запуск

```bash
py src/main.py --config config.ini
```

Или через `run.bat`.

## Тестирование

```bash
py -m unittest discover -s tests -v
```

## Основные функции

- `read_config()` — чтение конфигурации.
- `validate()` — проверка параметров.
- `parse_cli()` — чтение аргументов запуска.
- `main()` — запуск программы.

## Пример вывода

```text
package: bash
repository: https://archive.ubuntu.com/ubuntu/dists/noble/main/binary-amd64/Packages.xz
test_mode: False
version: 5.2.21-2ubuntu4
output: output/bash.png
```

На первом этапе реализована только конфигурация.
```
