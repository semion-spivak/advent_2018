import re
from itertools import starmap
from collections import defaultdict as dd

initial_pattern = re.compile(r'^initial state: ([#.]+)$', re.IGNORECASE)
tt_pattern = re.compile(r'^([#.]+) => ([#.])$')


with open('12.demo.in', 'r') as f:
    initial_state = initial_pattern.findall(f.readline())[0]
    f.readline()

    rules = dd(lambda: '.')
    for line in f:
        key, val = tt_pattern.findall(line)[0]
        rules[key] = val

    initial_state = f'...{initial_state}...'
    print(initial_state)
    start_at = -3
    for _ in range(20):
        new_state = []
        for i, pot in enumerate(initial_state, start=0):
            if i < 2 or i > len(initial_state) - 2:
                new_state.append(pot)
            else:
                new_state.append(rules[initial_state[i-2:i+3]])

        initial_state = ''.join(new_state)
        if initial_state.startswith('.#'):
            initial_state = f'.{initial_state}'
            start_at -= 1

        if initial_state.endswith('#.'):
            initial_state = f'{initial_state}.'

        print(initial_state)

    total = 0
    for i, pot in enumerate(initial_state, start=start_at):
        if pot == '#':
            total += i
    print(f'part 1: {total}')

