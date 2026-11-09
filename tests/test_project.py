"""Тесты этапов 1–4."""
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

class ProjectTests(unittest.TestCase):
    """Проверить анализ зависимостей. 1-4"""

    def test_config(self):
        """Читать настройки в INI. 1"""
        settings = read_config('config_test.ini')
        self.assertTrue(settings['test_mode'])

    def test_missing_config(self):
        """Отвергать отсутствующий INI. 1"""
        with self.assertRaises(ValueError):
            read_config('no_such_file.ini')

    def test_apt_parsing(self):
        """Извлечь прямые зависимости. 2"""
        text = (
            'Package: A\n'
            'Version: 1\n'
            'Depends: B (>= 1), C | D\n'
        )
        fields = parse_stanzas(text)[('A', '1')]
        self.assertEqual(get_direct(fields), ['B', 'C'])

    def test_bfs(self):
        """Построить граф рекурсивным BFS. 3"""
        data = load_test_graph('data/graph_chain.json')
        result = recursive_bfs('A', lambda n: data.get(n, []))
        self.assertEqual(len(result), 4)

    def test_cycle(self):
        """Обработать циклический граф. 3"""
        data = load_test_graph('data/graph_cycle.json')
        result = recursive_bfs('A', lambda n: data.get(n, []))
        self.assertEqual(len(result), 3)

    def test_order(self):
        """Разместить зависимости перед пакетом. 4"""
        data = load_test_graph('data/graph_chain.json')
        sequence, cycles = loading_order(data, 'A')
        self.assertEqual(sequence, ['D', 'B', 'C', 'A'])
        self.assertFalse(cycles)

    def test_order_cycle(self):
        """Обнаружить цикл в зависимостях. 4"""
        data = load_test_graph('data/graph_cycle.json')
        sequence, cycles = loading_order(data, 'A')
        self.assertEqual(len(sequence), 3)
        self.assertTrue(cycles)

if __name__ == '__main__':
    unittest.main()
