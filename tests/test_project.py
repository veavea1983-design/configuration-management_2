"""Тесты конфигурации и пакетов Ubuntu."""
import sys
import unittest
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parents[1] / 'src')
)

from config import read_config
from apt_data import parse_stanzas, get_direct

class ProjectTests(unittest.TestCase):
    """Проверить конфигурацию и зависимости. 1-2"""

    def test_config(self):
        """Читать настройки в INI. 1"""
        settings = read_config('config.ini')
        self.assertFalse(settings['test_mode'])

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

if __name__ == '__main__':
    unittest.main()
