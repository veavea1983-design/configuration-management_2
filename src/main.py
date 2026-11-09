"""CLI анализатора зависимостей Ubuntu."""
import argparse
import sys

from apt_data import download_index, parse_stanzas
from config import read_config
from graph import apt_provider, load_test_graph, recursive_bfs
from order import loading_order


def parse_cli(argv=None):
    """Прочитать путь к INI-файлу. 1"""
    parser = argparse.ArgumentParser(
        description='Анализ зависимостей apt'
    )
    parser.add_argument('--config', default='config.ini')
    return parser.parse_args(argv)

def make_provider(settings):
    """Подготовить источник прямых зависимостей. 3"""
    if settings['test_mode']:
        graph = load_test_graph(settings['repository'])
        if settings['package'] not in graph:
            raise ValueError('Пакет отсутствует в тестовом графе')
        return lambda name: graph.get(name, [])

    index = parse_stanzas(download_index(settings['repository']))
    return apt_provider(
        index, settings['package'], settings['version']
    )

def main(argv=None):
    """Вывести граф и порядок зависимостей. 1-4"""
    try:
        settings = read_config(parse_cli(argv).config)
        provider = make_provider(settings)
        root = settings['package']
        graph = recursive_bfs(root, provider)

        for node, children in graph.items():
            print(f'{node}: {", ".join(children)}')

        sequence, cycles = loading_order(graph, root)
        print('Оценочный порядок:', ' -> '.join(sequence))

        if cycles:
            print('Обнаружены циклы:', ', '.join(cycles))

    except (OSError, ValueError) as error:
        print(f'Ошибка: {error}', file=sys.stderr)
        return 1

    return 0

if __name__ == '__main__':
    raise SystemExit(main())
