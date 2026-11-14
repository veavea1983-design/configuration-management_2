"""Визуализация графа зависимостей."""
import re
import shutil
import subprocess
from pathlib import Path

def render_dot(graph):
    """Сформировать описание графа Graphviz. 5"""
    lines = ['digraph dependencies {', '  rankdir=LR;']

    for node, children in graph.items():
        for name in [node] + children:
            if not re.fullmatch(r'[A-Za-z0-9+.:_-]+', name):
                raise ValueError(f'Неверное имя пакета: {name}')

        lines.append(f'  "{node}";')
        for child in children:
            lines.append(f'  "{node}" -> "{child}";')

    lines.append('}')
    return '\n'.join(lines) + '\n'

def save_graph(graph, output):
    """Сохранить граф в форматах DOT и PNG. 5"""
    target = Path(output)
    if target.suffix.lower() != '.png':
        raise ValueError('Выходной файл должен быть PNG')

    dot_binary = shutil.which('dot')
    if not dot_binary:
        raise RuntimeError('Программа Graphviz не найдена')

    target.parent.mkdir(parents=True, exist_ok=True)
    dot_file = target.with_suffix('.dot')
    dot_file.write_text(render_dot(graph), encoding='utf-8')

    subprocess.run(
        [dot_binary, '-Tpng', str(dot_file), '-o', str(target)],
        check=True
    )
    return dot_file, target
