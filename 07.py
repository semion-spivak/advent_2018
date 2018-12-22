import re
from bisect import insort
from collections import defaultdict as dd

BASE_DURATION = 60
WORKERS = 5

# Step X must be finished before step Y can begin.
pattern = re.compile(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.")

def get_duration(name):
    '''
    >>> BASE_DURATION=0

    >>> get_duration('A')
    1
    >>> get_duration('Z')
    26
    '''
    return BASE_DURATION + ord(name) - 64

steps = {}

class Step:
    def __init__(self, name):
        self.name = name
        self.dep_list = []
        self.done = False
        self.duration = get_duration(name)
        self.started_at = None
    
    def start(self, t):
        self.started_at = t
    
    def can_end(self, t):
        return t - self.started_at >= self.duration
    
    def add_dep(self, dep):
        if dep not in self.dep_list:
            insort(self.dep_list, dep)
    
    def all_done(self):
        return self.done and self.all_deps_done()
    
    def all_deps_done(self):
        return all([d.all_done() for d in self.dep_list])
    
    def is_doable(self):
        return not self.done and self.started_at is None and self.all_deps_done()
    
    def __lt__(self, other):
        return self.name < other.name
    
    def __gte__(self, other):
        return self.name >= other.name
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __repr__(self):
        return f"name: {self.name}, deps: [{''.join([d.name for d in self.dep_list])}]"


with open('07.in', 'r') as f:
    for line in f:
        dep, name = pattern.findall(line)[0]
        if dep not in steps:
            steps[dep] = Step(dep)
        if name not in steps:
            steps[name] = Step(name)
        
        steps[name].add_dep(steps[dep])


ordered = []
while not all([s.done for s in steps.values()]):
    doable = []
    for name, s in steps.items():
        if s.is_doable():
            doable.append(name)
    name = sorted(doable)[0]
    steps[name].done = True
    ordered.append(name)
        

print(f"part 1: {''.join(ordered)}")

# part two
for name in steps.keys():
    steps[name].done = False

workers = {i:'.' for i in range(WORKERS)}
done = []
elapsed_time = -1
doable = []
while not all([s.done for s in steps.values()]):
    elapsed_time += 1
    for name, s in steps.items():
        if name not in doable and s.is_doable():
            doable.append(name)
    doable.sort()
    
    for i, task in workers.items():
        if task != '.':
            if steps[task].can_end(elapsed_time):
                steps[task].done = True
                done.append(task)
                workers[i] = '.'
                for i_name, i_s in steps.items():
                    if i_name not in doable and i_s.is_doable():
                        insort(doable, i_name)
                doable.sort()
            else:
                continue
        if doable:
            name = doable.pop(0)
            workers[i] = name
            steps[name].start(elapsed_time)
    # print(f"{elapsed_time}\t{' '.join([task for _, task in workers.items()])}\t{''.join(done)}")
    

print(f"part 2: {elapsed_time-1}")