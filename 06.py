import re
import pickle
from itertools import compress, product, filterfalse
from collections import defaultdict as dd

BORDER = 1
TOTAL_DISTANCE = 10000

class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def manhattan_distance(self, x, y):
        return abs(self.x - x) + abs(self.y - y)

    def __str__(self):
        return f"{self.x}, {self.y}"
    

coords_template = re.compile(r'(\d+), (\d+)')

coords = []
with open('06.in', 'r') as f:
    for line in f:
        coords.append(Point(*coords_template.findall(line)[0]))


min_x = min([c.x for c in coords]) - BORDER
max_x = max([c.x for c in coords]) + BORDER
min_y = min([c.y for c in coords]) - BORDER
max_y = max([c.y for c in coords]) + BORDER

def is_on_border(x, y):
    return any([x == min_x, x == max_x, y == min_y, y == max_y])

def compress_distances(d_list: list):
    mask = []
    min_d = min([_d for _, _d in d_list])
    for _, d in d_list:
        mask.append(d == min_d)
    return list(compress(d_list, mask))

starmap = dd(list)
infinite_regions = set()

map_iter = lambda: product(range(min_x, max_x+1), range(min_y, max_y+1))

for xy in map_iter():
    for i, c in enumerate(coords):
        d = c.manhattan_distance(*xy)
        starmap[xy].append((i, d))

# intermediate starmap storage on disk
with open('06_starmap.pickle', 'wb') as pickle_file:
    pickle.dump(starmap, pickle_file)

for xy in map_iter():
    c_d_list = compress_distances(starmap[xy])
    if len(c_d_list) == 1:
        starmap[xy] = c_d_list
        if is_on_border(*xy):
            infinite_regions.add(c_d_list[0][0])
    else:
        starmap[xy] = []
    

hostile_regions = dd(int)
for xy, d_list in starmap.items():
    for i, d in filterfalse(lambda x: x[0] in infinite_regions, d_list):
        hostile_regions[i] += 1

print(f"part 1: {max(hostile_regions.values())}")

# load pickled starmap from earlier
with open('06_starmap.pickle', 'rb') as pickle_file:
    starmap = pickle.load(pickle_file)

friendly_region_size = 0
for xy in map_iter():
    if sum([d for i, d in starmap[xy]]) < TOTAL_DISTANCE:
        friendly_region_size +=1 

print(f"part 2: {friendly_region_size}")
