"""Получение метаданных Ubuntu без использования apt."""
import gzip
import lzma
import re
from urllib.request import urlopen

def download_index(url):
    """Скачать и распаковать индекс Packages. 2"""
    with urlopen(url, timeout=30) as response:
        content = response.read()
    if url.lower().endswith('.xz'):
        return lzma.decompress(content).decode('utf-8')
    if url.lower().endswith('.gz'):
        return gzip.decompress(content).decode('utf-8')
    return content.decode('utf-8')

def parse_stanzas(text):
    """Разобрать абзацы формата Debian control. 2"""
    packages = {}
    for paragraph in re.split(r'\n\s*\n', text):
        fields = {}
        current = None
        for line in paragraph.splitlines():
            if line.startswith((' ', '\t')) and current:
                fields[current] += ' ' + line.strip()
            elif ': ' in line:
                key, value = line.split(': ', 1)
                current = key
                fields[key] = value
        name = fields.get('Package')
        version = fields.get('Version')
        if name and version:
            packages[(name, version)] = fields
    return packages

def dependency_names(text):
    """Извлечь имена прямых зависимостей. 2"""
    names = []
    for group in text.split(','):
        alternatives = group.split('|')
        if not group.strip():
            continue
        first = alternatives[0].strip()
        match = re.match(r'^([a-zA-Z0-9+.-]+)', first)
        if match:
            names.append(match.group(1))
    return list(dict.fromkeys(names))

def get_direct(fields):
    """Получить Depends и Pre-Depends пакета. 2"""
    parts = [fields.get('Pre-Depends', ''), fields.get('Depends', '')]
    return dependency_names(', '.join(x for x in parts if x))

def select_version(index, name, exact=None):
    """Найти указанную версию пакета в индексе. 2"""
    if exact:
        return index.get((name, exact))
    available = [
        data for (n, _), data in index.items() if n == name
    ]
    return available[0] if available else None
