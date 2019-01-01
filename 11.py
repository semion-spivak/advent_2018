from itertools import product, tee

GRID_SIZE = 300


def get_power_level(x, y, sn):
    # global grid_serial_number
    rack_id = x + 10
    power_level = rack_id * y
    power_level += sn
    power_level *= rack_id
    power_level = (power_level // 100) % 10
    power_level -= 5
    return power_level


def main():
    with open('11.in', 'r') as f:
        sn = int(f.read())

    grid = {}
    known_levels = set()

    for x, y in product(*tee(range(1, GRID_SIZE+1), 2)):
        level = get_power_level(x, y, sn)
        grid[(x, y)] = level
        known_levels.add(level)

    max_charge = min(known_levels) * 9
    strongest_cell = (None, None)
    strongest_size = None
    for s in range(2, GRID_SIZE+1):
        for x in range(1, GRID_SIZE+1-s, 1):
            for y in range(1, GRID_SIZE+1-s, 1):
                cell_charge = []
                for i, j in product(*tee(range(s), 2)):
                    cell_charge.append(grid[(x+i, y+j)])
                if sum(cell_charge) > max_charge:
                    max_charge = sum(cell_charge)
                    strongest_cell = (x, y)
                    strongest_size = s

        if s == 3:
            print(f"part 1: {strongest_cell}")

    print(f"part 2: {strongest_cell},{strongest_size}")

if __name__ == '__main__':
    main()




