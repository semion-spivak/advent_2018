import re
from collections import deque


with open('09.in', 'r') as f:
    players_cnt, last_marble_value = tuple(map(int, re.findall(r'^(\d+) players; last marble is worth (\d+) points', f.readline())[0]))

# uncomment below for part 2
# last_marble_value *= 100 

pool = deque(range(0, last_marble_value+1))
ring = deque()
players = {i: 0 for i in range(1, players_cnt+1)}

# set the 0 marble
ring.append(pool.popleft())

while pool:
    for i in players.keys():
        try:
            marble = pool.popleft()
        except IndexError:
            break
        if marble % 23 == 0:
            players[i] += marble
            ring.rotate(7)
            players[i] += ring.pop()
            ring.rotate(-1)
            continue
        ring.rotate(-1)
        ring.append(marble)

print(max(players.values()))
