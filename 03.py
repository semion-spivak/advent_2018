from collections import defaultdict as dd
from itertools import product, chain
from re import compile

pattern = compile(r"^#(?P<claim_id>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)$")
SIDE = 1000

def to_abs_list(left, top, width, height):
    return product(range(left, left+width), range(top, top+height))

with open('03.in', 'r') as f:
    tiles = dd(list)
    for line in f:
        match = pattern.match(line).groupdict()
        for t in to_abs_list(int(match['left']), int(match['top']), int(match['width']), int(match['height'])):
            tiles[f"{t[0]}:{t[1]}"].append(int(match['claim_id']))
    
    print(f"part 1: {len([x for x in tiles.values() if len(x) > 1])}")

    singles = set([y[0] for x, y in tiles.items() if len(y) == 1])
    multiples = set(chain(*[y for x, y in tiles.items() if len(y) > 1]))

    print(f"part 2: {(singles - multiples).pop()}")