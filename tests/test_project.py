"""Тесты конфигурации."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from config import read_config

class ProjectTests(unittest.TestCase):
    """Проверить настройки приложения. 1"""

    def test_config(self):
        """Читать настройки в INI. 1"""
        settings = read_config('config.ini')
        self.assertFalse(settings['test_mode'])

    def test_missing_config(self):
        """Отвергать отсутствующий INI. 1"""
        with self.assertRaises(ValueError):
            read_config('no_such_file.ini')

if __name__ == '__main__':
    unittest.main()
