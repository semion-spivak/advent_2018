from collections import Counter
from itertools import combinations

twos = 0
threes = 0
with open('02.in', 'r') as f:
    for line in f:
        c = Counter(line).values()
        twos += int(2 in c)
        threes += int(3 in c)
    print(f"part 1: {twos * threes}")

    f.seek(0)
    comb = combinations(f, 2)

    for a, b in comb:
        similar = [j for j, k in zip(a, b) if j == k]
        if len(a) - len(similar) == 1:
            print(f"part 2: {''.join(similar)}")

