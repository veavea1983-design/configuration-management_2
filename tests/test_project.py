"""Тесты этапов 1–5."""
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / 'src')
)

from config import read_config
from apt_data import parse_stanzas, get_direct
from graph import recursive_bfs, load_test_graph
from order import loading_order
from visual import render_dot

class ProjectTests(unittest.TestCase):
    """Проверить анализ зависимостей. 1-5"""

    def test_config(self):
        """Проверить чтение настроек. 1"""
        settings = read_config('config_test.ini')
        self.assertTrue(settings['test_mode'])

    def test_missing_config(self):
        """Проверить отсутствие INI. 1"""
        with self.assertRaises(ValueError):
            read_config('no_such_file.ini')

    def test_apt_parsing(self):
        """Проверить прямые зависимости. 2"""
        text = (
            'Package: A\n'
            'Version: 1\n'
            'Depends: B (>= 1), C | D\n'
        )
        fields = parse_stanzas(text)[('A', '1')]
        self.assertEqual(get_direct(fields), ['B', 'C'])

    def test_bfs(self):
        """Проверить рекурсивный BFS. 3"""
        data = load_test_graph('data/graph_chain.json')
        result = recursive_bfs('A', lambda n: data.get(n, []))
        self.assertEqual(len(result), 4)

    def test_cycle(self):
        """Проверить циклический граф. 3"""
        data = load_test_graph('data/graph_cycle.json')
        result = recursive_bfs('A', lambda n: data.get(n, []))
        self.assertEqual(len(result), 3)

    def test_order(self):
        """Проверить порядок зависимостей. 4"""
        data = load_test_graph('data/graph_chain.json')
        sequence, cycles = loading_order(data, 'A')
        self.assertEqual(sequence, ['D', 'B', 'C', 'A'])
        self.assertFalse(cycles)

    def test_order_cycle(self):
        """Проверить обнаружение цикла. 4"""
        data = load_test_graph('data/graph_cycle.json')
        sequence, cycles = loading_order(data, 'A')
        self.assertEqual(len(sequence), 3)
        self.assertTrue(cycles)

    def test_graphviz(self):
        """Проверить описание Graphviz DOT. 5"""
        graph = {'A': ['B'], 'B': []}
        result = render_dot(graph)
        self.assertIn('"A" -> "B";', result)
        self.assertIn('digraph dependencies', result)

if __name__ == '__main__':
    unittest.main()
