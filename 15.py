from collections import OrderedDict
import networkx as nx

cave = OrderedDict()
graph = nx.OrderedGraph()


class Unit:
    enemy_class = None
    range_search = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attack_power = 3
        self.hit_points = 200


class Goblin(Unit):
    enemy_class = 'Elf'


class Elf(Unit):
    enemy_class = 'Goblin'


cell_type = {'.': lambda x, y: None,
             'E': lambda x, y: Elf(x, y),
             'G': lambda x, y: Goblin(x, y)}


def main():
    with open('15_input.txt', 'r') as f:
        for x, line in enumerate(f, start=1):
            for y, cell in enumerate(line.strip(), start=1):
                if cell == '#':
                    continue
                cave[(x, y)] = cell_type[cell](x, y)
                graph.add_node((x, y))
    for (x, y), cell in cave.items():
        for dx, dy in Unit.range_search:
            if (x + dx, y + dy) in cave.keys():
                graph.add_edge((x, y), (x + dx, y + dy))

    while True:
        idx, unit = [(idx, n) for idx, n in cave.items() if n is not None][0]
        foes = {idx for idx, n in cave.items() if n.__class__.__name__==unit.enemy_class}
        allies = {idx for idx, n in cave.items() if n.__class__==unit.__class__} ^ {idx}
        empty_cells = (set(cave.keys()) ^ allies) ^ foes
        foes_paths = []
        for foe in foes:
            try:
                path = nx.dijkstra_path(graph.subgraph(empty_cells | {foe}), idx, foe)[1:]
            except nx.NetworkXNoPath:
                continue
            foes_paths.append(path)
        pass


if __name__ == '__main__':
    main()
