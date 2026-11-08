"""Чтение конфигурации инструмента."""
import configparser
from pathlib import Path
from urllib.parse import urlparse


def read_config(path):
    """Прочитать параметры из INI. 1"""
    parser = configparser.ConfigParser()
    if not Path(path).is_file():
        raise ValueError('Файл INI не найден')
    try:
        parser.read(path, encoding='utf-8')
        if not parser.has_section('settings'):
            raise ValueError('Нет секции [settings]')
        block = parser['settings']
        params = {
            'package': block.get('package', '').strip(),
            'repository': block.get('repository', '').strip(),
            'test_mode': block.getboolean('test_mode'),
            'version': block.get('version', '').strip(),
            'output': block.get('output', '').strip(),
        }
    except configparser.Error as error:
        raise ValueError(f'Некорректный INI: {error}') from error
    validate(params)
    return params


def validate(params):
    """Проверить все настройки. 1"""
    if not params['package']:
        raise ValueError('Не указано имя пакета')
    if not params['version']:
        raise ValueError('Не указана версия пакета')
    source = params['repository']
    if not source:
        raise ValueError('Не указан репозиторий')
    if params['test_mode']:
        if not Path(source).is_file():
            raise ValueError('Тестовый репозиторий не найден')
        if not params['package'].isupper():
            raise ValueError('Тестовые пакеты: A-Z')
    else:
        url = urlparse(source)
        if url.scheme not in ('http', 'https') or not url.netloc:
            raise ValueError('Неверный URL репозитория')
    if Path(params['output']).suffix.lower() != '.png':
        raise ValueError('Результат должен иметь расширение .png')
