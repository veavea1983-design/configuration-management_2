"""CLI анализатора зависимостей Ubuntu."""
import argparse
import sys
from config import read_config

def parse_cli(argv=None):
    """Прочитать путь к INI-файлу. 1"""
    parser = argparse.ArgumentParser(
        description='Анализ зависимостей apt'
    )
    parser.add_argument(
        '--config',
        default='config.ini'
    )
    return parser.parse_args(argv)

def main(argv=None):
    """Вывести настройки анализатора. 1"""
    try:
        settings = read_config(parse_cli(argv).config)
        for key, value in settings.items():
            print(f'{key}: {value}')
    except (OSError, ValueError) as error:
        print(f'Ошибка: {error}', file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
