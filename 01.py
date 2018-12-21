from collections import defaultdict as dd

with open('01.in', 'r') as f:
    print(f"part 1: {sum(map(int, f))}")

    counter = dd(int)
    freq = 0
    counter[freq] += 1
    found = False

    while not found:
        f.seek(0)
        for n in f:
            freq += int(n)
            counter[freq] += 1
            if counter[freq] == 2:
                print(f"part 2: {freq}")
                found = True
                break
