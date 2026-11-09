"""Построение графа зависимостей."""
import json
import re
from collections import deque

from apt_data import get_direct, select_version

def load_test_graph(path):
    """Прочитать тестовый граф из JSON. 3"""
    with open(path, encoding='utf-8') as file:
        graph = json.load(file)

    if not isinstance(graph, dict):
        raise ValueError('Граф должен быть объектом JSON')

    for node, children in graph.items():
        if not re.fullmatch(r'[A-Z]+', node):
            raise ValueError('Имена пакетов должны быть A-Z')
        if not isinstance(children, list):
            raise ValueError('Зависимости должны быть списком')
        for child in children:
            if not isinstance(child, str):
                raise ValueError('Неверное имя зависимости')
            if not re.fullmatch(r'[A-Z]+', child):
                raise ValueError('Зависимости должны называться A-Z')

    return graph

def recursive_bfs(root, provider):
    """Построить граф рекурсивным BFS. 3"""
    result = {}
    visited = set()
    queue = deque([root])

    def next_level():
        """Обработать следующий уровень очереди. 3"""
        if not queue:
            return

        count = len(queue)

        for _ in range(count):
            node = queue.popleft()

            if node in visited:
                continue

            visited.add(node)
            children = provider(node)
            result[node] = list(children)

            for child in children:
                if child not in visited and child not in queue:
                    queue.append(child)

        next_level()

    next_level()
    return result

def apt_provider(index, root, version):
    """Получить зависимости из индекса Ubuntu. 3"""
    if select_version(index, root, version) is None:
        raise ValueError('Пакет нужной версии не найден')

    def dependencies(name):
        """Найти зависимости указанного пакета. 3"""
        exact = version if name == root else None
        fields = select_version(index, name, exact)
        return get_direct(fields) if fields else []

    return dependencies
