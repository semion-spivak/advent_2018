from itertools import count, chain
import networkx as nx

cave, elves, goblins = None, None, None


class Unit:
    foes = nx.Graph()
    allies = nx.Graph()

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.attack_power = 3
        self.hit_points = 200
        self.foes_paths = []

    def find_paths_to_foes(self):
        global cave
        self.foes_paths = []
        cave_without_allies = cave.restricted_view(self.allies.nodes())
        for foe in self.foes.nodes():
            try:
                self.foes_paths.append(cave_without_allies.shortest_path(foe))
            except nx.NetworkXNoPath:
                pass


class Elf(Unit):
    global elves, goblins
    allies = elves
    foes = goblins


class Goblin(Unit):
    global elves, goblins
    allies = goblins
    foes = elves


def main():
    global cave, elves, goblins
    x, y = 0, 0
    coords = {}
    cave = nx.Graph()

    goblins = nx.Graph()
    elves = nx.Graph()

    with open('15.in', 'r') as f:
        for y, line in zip(count(), f):
            for x, cell in enumerate(line.rstrip('\n')):
                if cell == '#':
                    coords[(x, y)] = cell
                    continue
                elif cell == 'G':
                    goblins.add_node((x, y), obj=Goblin(x, y))
                elif cell == 'E':
                    elves.add_node((x, y), obj=Elf(x, y))
                coords[(x, y)] = '.'
                cave.add_node((x, y))

    for i in range(x+1):
        for j in range(y+1):
            if coords.get((i, j)) == '#':
                continue
            cave.add_star(
                chain([(i, j)],
                      filter(lambda _o: coords.get(_o, '#') != '#', [(i, j-1), (i, j+1), (i-1, j), (i+1, j)])))

    pass


if __name__ == '__main__':
    main()
