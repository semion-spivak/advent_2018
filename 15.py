from itertools import count, chain, product
from operator import itemgetter
import networkx as nx


class NoMoreRounds(Exception): pass


class Unit:
    def __init__(self, node, foes:nx.Graph, allies:nx.Graph, cave:nx.Graph):
        self.node = node
        self.attack_power = 3
        self.hit_points = 200
        self.foes_paths = []
        self.foes = foes
        self.adjacent_foes = set()
        self.allies = allies
        self.cave = cave

    def find_adjacent_foes(self):
        # if no more enemies - finish the game
        if len(self.foes.nodes()) == 0:
            raise NoMoreRounds

        self.adjacent_foes = set(self.cave.neighbors(self.node)).intersection(set(self.foes.nodes.keys()))

    def find_paths_to_foes(self):
        if self.adjacent_foes:
            return

        # find nodes that cannot be traversed during path finding - it's all Units, excluding self
        nontraversal = set(chain(self.allies.nodes(), self.foes.nodes())) - {self.node}
        self.foes_paths = []
        self.adjacent_foes.clear()
        for foe in self.foes.nodes():
            # exclude foe from non-traversal nodes and make a restricted view of a cave
            sub = nx.restricted_view(self.cave, nontraversal - {foe}, [])
            try:
                path = nx.shortest_path(sub, source=self.node, target=foe)[1:-1]
                if path:
                    self.foes_paths.append(path)

            except nx.NetworkXNoPath:
                continue

    def approach(self):
        if self.adjacent_foes:
            return
        # choose shortest path & by reading order
        if len(self.foes_paths) > 1:
            self.foes_paths = sorted(self.foes_paths, key=lambda p: p[0][0])
            self.foes_paths = sorted(self.foes_paths, key=lambda p: p[0][1])
            self.foes_paths = sorted(self.foes_paths, key=lambda p: len(p))
        try:
            path = self.foes_paths[0]
        except IndexError:
            return
        self.allies.remove_node(self.node)
        self.node = path[0]
        self.allies.add_node(self.node, obj=self)
        self.find_adjacent_foes()

    def attack(self):
        if not self.adjacent_foes:
            return
        # choose adjacent foe with minimal health or first by reading order
        self.adjacent_foes = sorted(self.adjacent_foes, key=itemgetter(0))
        self.adjacent_foes = sorted(self.adjacent_foes, key=itemgetter(1))
        self.adjacent_foes = sorted(list(self.adjacent_foes),
                                    key=lambda f: self.foes.nodes._nodes[f]['obj'].hit_points)

        foe = self.adjacent_foes[0]
        self.foes.nodes._nodes[foe]['obj'].handle_damage(self.attack_power)

    def handle_damage(self, damage):
        self.hit_points -= damage
        if self.hit_points <= 0:
            self.die()

    def tick(self):
        self.find_adjacent_foes()
        self.find_paths_to_foes()
        self.approach()
        self.attack()

    def die(self):
        self.allies.remove_node(self.node)


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

    with open('15.demo.in', 'r') as f:
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
    done = False
    rounds = 0
    while not done:
        # sort Units by reading order
        units = sorted(chain(elves.nodes(data=True), goblins.nodes(data=True)), key=lambda tup: tup[0][0])
        units = sorted(units, key=lambda tup: tup[0][1])
        for _, unit in units:
            try:
                unit['obj'].tick()
                rounds += 1
            except NoMoreRounds:
                done = True
                break

    print(f"part 1: {rounds * sum([unit['obj'].hit_points for _, unit in chain(elves.nodes(data=True), goblins.nodes(data=True))])}")


if __name__ == '__main__':
    main()

