"""Определение порядка загрузки зависимостей."""

def loading_order(graph, root):
    """Сформировать порядок зависимостей. 4"""
    active = set()
    done = set()
    sequence = []
    cycles = []

    def visit(node):
        """Обработать пакет и его зависимости. 4"""
        if node in active:
            cycles.append(node)
            return

        if node in done:
            return

        active.add(node)

        for child in graph.get(node, []):
            visit(child)

        active.remove(node)
        done.add(node)
        sequence.append(node)

    visit(root)
    return sequence, cycles
