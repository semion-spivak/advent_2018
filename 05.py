from itertools import chain, filterfalse, islice
from functools import partial

def opposit_charge(a, b):
    res = abs(a - b) == 32
    return res

def remove_letter(line, letter):
    upper = ord(chr(letter).upper())
    lower = ord(chr(letter).lower())
    return list(filterfalse(lambda x: x in (upper, lower), line))

def wrap(poly):
    no_more_matches = False
    while not no_more_matches:
        if len(poly) <= 1:
            break
        for i in range(0, len(poly)-1):
            if opposit_charge(poly[i], poly[i+1]):
                poly = list(chain(islice(poly, 0, i), islice(poly, i+2, None)))
                break
        else:
            no_more_matches = True
    return poly

with open('05.in', 'r') as f:
    p = list(map(ord, f.readline()))

wrapped = wrap(p)
print(f"part 1: {len(wrapped)}")

len_list = []
for l in range(ord('a'), ord('z')+1):
    current_poly = remove_letter(wrapped, l)
    len_list.append(len(wrap(current_poly)))

print(f"part 2: {min(len_list)}")
