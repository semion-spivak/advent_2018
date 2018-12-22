import re
from bisect import insort
from collections import defaultdict as dd

# Step X must be finished before step Y can begin.
pattern = re.compile(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.")

steps = {}

class Step:
    def __init__(self, name):
        self.name = name
        self.dep_list = []
        self.done = False
    
    def add_dep(self, dep):
        if dep not in self.dep_list:
            insort(self.dep_list, dep)
    
    def all_done(self):
        return self.done and all([d.all_done() for d in self.dep_list])
    
    def is_doable(self):
        return not self.done and all([d.all_done() for d in self.dep_list])
    
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