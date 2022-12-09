from itertools import combinations
import numpy as np

list = [0.95, 0.99, 0.97]

a = (1-(1-list[0])*(1-list[1])*(1-list[2]))*(1-(1-list[0])*(1-list[1])*(1-list[2]))

print(a)
combs = []
for i in range(len(list)):
    els = [list(x) for x in combinations(list, i) if len(x) < len(list) ]
    combs.extend(els)

print(combs)