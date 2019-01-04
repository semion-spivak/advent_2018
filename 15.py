from itertools import count, chain, product
import networkx as nx


class Unit:
    def __init__(self, node, foes=None, allies=None, cave: nx.Graph = None):
        self.node = node
        self.attack_power = 3
        self.hit_points = 200
        self.foes_paths = []
        self.foes = foes
        self.allies = allies
        self.cave = cave

    def find_paths_to_foes(self):
        nontraversal = set(chain(self.allies.nodes(), self.foes.nodes())) - {self.node}
        self.foes_paths = []
        for foe in self.foes.nodes():
            sub = nx.restricted_view(self.cave, nontraversal - {foe}, [])
            self.foes_paths.append(nx.shortest_path(sub, source=self.node, target=foe))

    def approach(self):
        pass

    def attack(self):
        pass

    def tick(self):
        self.find_paths_to_foes()


class Elf(Unit):
    pass


class Goblin(Unit):
    pass


def main():
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
                    goblins.add_node((x, y), obj=Goblin((x, y), foes=elves, allies=goblins, cave=cave))
                elif cell == 'E':
                    elves.add_node((x, y), obj=Elf((x, y), foes=goblins, allies=elves, cave=cave))
                coords[(x, y)] = '.'
                cave.add_node((x, y))

    for i, j in product(range(x+1), range(y+1)):
        if coords.get((i, j)) == '#':
            continue
        nx.add_star(cave, chain([(i, j)],
                  filter(lambda _o: coords.get(_o, '#') != '#', [(i, j-1), (i, j+1), (i-1, j), (i+1, j)])))

    for (x, y), unit in chain(elves.nodes(data=True), goblins.nodes(data=True)):
        unit['obj'].tick()

    pass


if __name__ == '__main__':
    main()

