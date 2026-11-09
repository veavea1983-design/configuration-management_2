"""CLI анализатора зависимостей Ubuntu."""
import argparse
import sys

from config import read_config
from apt_data import (
    download_index,
    get_direct,
    parse_stanzas,
    select_version,
)

def parse_cli(argv=None):
    """Прочитать путь к INI-файлу. 1"""
    parser = argparse.ArgumentParser(
        description='Анализ зависимостей apt'
    )
    parser.add_argument('--config', default='config.ini')
    return parser.parse_args(argv)

def main(argv=None):
    """Получить и вывести прямые зависимости. 1-2"""
    try:
        settings = read_config(parse_cli(argv).config)
        if settings['test_mode']:
            raise ValueError(
                'Тестовый граф поддерживается с этапа 3'
            )

        raw = download_index(settings['repository'])
        index = parse_stanzas(raw)

        name = settings['package']
        version = settings['version']
        fields = select_version(index, name, version)

        if fields is None:
            raise ValueError('Пакет нужной версии не найден')

        dependencies = get_direct(fields)
        print('Прямые зависимости:', ', '.join(dependencies))

    except (OSError, ValueError) as error:
        print(f'Ошибка: {error}', file=sys.stderr)
        return 1

    return 0

if __name__ == '__main__':
    raise SystemExit(main())
