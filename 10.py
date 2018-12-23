"""
This requires `pip install recordclass`

"""

import re
from recordclass import recordclass
import curses
import pickle


# position=<-31761,  10798> velocity=< 3, -1>
pattern = re.compile(r'position=< ?(-?\d+),  ?(-?\d+)> velocity=< ?(-?\d+),  ?(-?\d+)>')

Point = recordclass('Point', 'x y vel_x vel_y')

points = []
with open('10.in', 'r') as f:
    for line in f:
        points.append(Point(*tuple(map(int, pattern.findall(line)[0]))))

with open('10.points.pickle', 'wb') as pf:
    pickle.dump(points, pf)


def get_box_height():
    min_y = min([p.y for p in points])
    max_y = max([p.y for p in points])
    return max_y - min_y


t = 0
t_found = None
initial_height = h = get_box_height()
while True:
    t += 1
    for i, point in enumerate(points):
        points[i].x += point.vel_x
        points[i].y += point.vel_y

    new_h = get_box_height()
    if new_h < h:
        h = new_h
        t_found = t
    if new_h > initial_height:
        break

with open('10.points.pickle', 'rb') as pf:
    points = pickle.load(pf)

for i, p in enumerate(points):
    points[i].x += p.vel_x * t_found
    points[i].y += p.vel_y * t_found

min_x = min([p.x for p in points])
min_y = min([p.y for p in points])

scr = curses.initscr()
scr.keypad(0)
curses.noecho()

for p in points:
    scr.addch(p.y - min_y, p.x - min_x, '*')

scr.addstr(h+3, 0, f"part 2: {t_found}")
scr.addstr(h+4, 0, "[press any key to exit]")
scr.refresh()
scr.getch()

curses.endwin()

