from itertools import chain

def are_opposit_charge(a, b):
    res = abs(a - b) == 32
    # print(a, b, res)
    return res



with open('05.in', 'r') as f:
    poly = list(map(ord, f.readline()))
    # poly = list(map(ord, 'dabAcCaCBAcCcaDA'))
    # print("".join(map(chr, poly)))
    initial_len = len(poly)
    
    no_more_matches = False
    while not no_more_matches:
        if len(poly) <= 1:
            break
        for i in range(0, len(poly)-1):
            if are_opposit_charge(poly[i], poly[i+1]):
                # print(i, i+1)
                poly = list(chain(poly[:i], poly[i+2:]))
                # print("".join(map(chr, poly)))
                break
        else:
            no_more_matches = True
    # print("".join(map(chr, poly)))
    print(f"part 1: {len(poly)}")
    
    

