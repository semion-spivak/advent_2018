from collections import deque
import sys

sys.setrecursionlimit(1500)

with open('08.in', 'r') as f:
    data = deque(map(int, f.readline().split(' ')))

class Node:
    def __init__(self):
        self.children = []
        self.metadata = []
    
    def meta_sum(self):
        return sum(self.metadata) + sum([c.meta_sum() for c in self.children])
    
    def value(self):
        if not self.children:
            return sum(self.metadata)
        m_sum = 0
        for i in map(lambda x: x-1, self.metadata):
            if i == -1:
                continue
            try:
                cnode = self.children[i]
            except IndexError:
                continue
            m_sum += cnode.value()
        return m_sum

    

def load():
    children_len = data.popleft()
    meta_len = data.popleft()

    node = Node()
    for _ in range(children_len):
        node.children.append(load())
    
    for _ in range(meta_len):
        node.metadata.append(data.popleft())

    return node

root = load()

print(f"part 1: {root.meta_sum()}")

print(f"part 2: {root.value()}")
