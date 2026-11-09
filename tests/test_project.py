"""Тесты конфигурации и графа зависимостей."""
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / 'src')
)

from config import read_config
from apt_data import parse_stanzas, get_direct
from graph import recursive_bfs, load_test_graph

class ProjectTests(unittest.TestCase):
    """Проверить анализ зависимостей. 1-3"""

    def test_config(self):
        """Читать настройки в INI. 1"""
        settings = read_config('config_test.ini')
        self.assertTrue(settings['test_mode'])

    def test_missing_config(self):
        """Отвергать отсутствующий INI. 1"""
        with self.assertRaises(ValueError):
            read_config('no_such_file.ini')

    def test_apt_parsing(self):
        """Извлечь прямые зависимости пакета. 2"""
        text = (
            'Package: A\n'
            'Version: 1\n'
            'Depends: B (>= 1), C | D\n'
        )
        fields = parse_stanzas(text)[('A', '1')]
        self.assertEqual(get_direct(fields), ['B', 'C'])

    def test_bfs(self):
        """Построить полный граф BFS с рекурсией. 3"""
        data = load_test_graph('data/graph_chain.json')
        result = recursive_bfs('A', lambda n: data.get(n, []))
        self.assertEqual(len(result), 4)
        self.assertEqual(result['A'], ['B', 'C'])
        self.assertEqual(result['B'], ['D'])
        self.assertEqual(result['C'], ['D'])

    def test_cycle(self):
        """Завершить BFS на циклическом графе. 3"""
        data = load_test_graph('data/graph_cycle.json')
        result = recursive_bfs('A', lambda n: data.get(n, []))
        self.assertEqual(len(result), 3)
        self.assertEqual(result['C'], ['A'])


if __name__ == '__main__':
    unittest.main()
