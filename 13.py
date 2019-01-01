from itertools import count
from collections import deque, defaultdict as dd
from copy import copy
from operator import attrgetter


bearings = {'^': deque('^>v<'),
            '>': deque('>v<^'),
            'v': deque('v<^>'),
            '<': deque('<^>v')}

next_steps = {'^': lambda x, y: (x, y-1),
              '>': lambda x, y: (x+1, y),
              'v': lambda x, y: (x, y+1),
              '<': lambda x, y: (x-1, y)}

grid = dd(lambda: dd(lambda: ' '))
carts = []
id_counter = count()


class Collision(Exception): pass


class Cart:
    def __init__(self, x, y, bearing):
        self.cross_count = 0
        self.bearing = copy(bearings[bearing])
        self.x = x
        self.y = y
        self.id = next(id_counter)
        self.removed = False

    def __repr__(self):
        return f"x={self.x},y={self.y},bearing={self.bearing}"

    def tick(self):
        global grid
        global carts
        self.x, self.y = next_steps[self.bearing[0]](self.x, self.y)

        for c in carts:
            if c.x == self.x and c.y == self.y and c.id != self.id:
                self.removed = c.removed = True
                raise Collision(f'{self.x},{self.y}')

        cell = grid[self.x][self.y]

        if cell in '|-':
            pass
        elif cell == '+':
            self.cross_count += 1
            if self.cross_count % 3 == 1:
                self.bearing.rotate(1)
            elif self.cross_count % 3 == 0:
                self.bearing.rotate(-1)
        elif cell == '\\':
            if self.bearing[0] in '><':
                self.bearing.rotate(-1)
            else:
                self.bearing.rotate(1)
        elif cell == '/':
            if self.bearing[0] in '><':
                self.bearing.rotate(1)
            else:
                self.bearing.rotate(-1)


def main():
    global grid, carts
    with open('13.in', 'r') as f:
        for y, line in zip(count(), f):
            for x, symbol in enumerate(line):
                if symbol in '<>':
                    grid[x][y] = '-'
                    carts.append(Cart(x, y, symbol))
                elif symbol in '^v':
                    grid[x][y] = '|'
                    carts.append(Cart(x, y, symbol))
                elif symbol:
                    grid[x][y] = symbol

        found = 0
        while len(carts) > 1:
            for c in carts:
                try:
                    c.tick()
                except Collision as e:
                    found += 1
                    if found == 1:
                        print(f'part 1: {e}')

            carts = sorted([_c for _c in carts if not _c.removed], key=attrgetter('x', 'y'))

        print(f'part 2: {carts[0].x},{carts[0].y}')


if __name__ == '__main__':
    main()



