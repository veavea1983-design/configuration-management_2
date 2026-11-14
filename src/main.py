"""CLI анализатора зависимостей Ubuntu."""
import argparse
import subprocess
import sys

from apt_data import download_index, parse_stanzas
from config import read_config
from graph import apt_provider, load_test_graph, recursive_bfs
from order import loading_order
from visual import save_graph

def parse_cli(argv=None):
    """Прочитать путь к INI-файлу. 1"""
    parser = argparse.ArgumentParser(
        description='Анализ зависимостей apt'
    )
    parser.add_argument('--config', default='config.ini')
    return parser.parse_args(argv)

def make_provider(settings):
    """Подготовить источник зависимостей. 2-3"""
    if settings['test_mode']:
        graph = load_test_graph(settings['repository'])
        if settings['package'] not in graph:
            raise ValueError('Пакет отсутствует в тестовом графе')
        return lambda name: graph.get(name, [])

    index = parse_stanzas(download_index(settings['repository']))
    return apt_provider(
        index, settings['package'], settings['version']
    )

def run(settings):
    """Построить и визуализировать граф. 3-5"""
    root = settings['package']
    provider = make_provider(settings)
    graph = recursive_bfs(root, provider)

    for node, children in graph.items():
        print(f'{node}: {", ".join(children)}')

    sequence, cycles = loading_order(graph, root)
    print('Оценочный порядок:', ' -> '.join(sequence))

    if cycles:
        print('Обнаружены циклы:', ', '.join(cycles))

    dot_file, png_file = save_graph(graph, settings['output'])
    print('Файл DOT:', dot_file)
    print('Файл PNG:', png_file)

def main(argv=None):
    """Запустить анализ зависимостей. 1-5"""
    try:
        settings = read_config(parse_cli(argv).config)
        run(settings)
    except (
        OSError,
        ValueError,
        RuntimeError,
        subprocess.CalledProcessError
    ) as error:
        print(f'Ошибка: {error}', file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
