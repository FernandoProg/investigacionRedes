from itertools import chain, combinations
import numpy as np
from functools import reduce
import matplotlib.pyplot as plt

def powerset(list_name):
    s = list(list_name)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


confmin = 0.95
conf = [0.95, 0.99, 0.97]
delays = [0.8, 3, 2]

a = (1-(1-conf[0])*(1-conf[1])*(1-conf[2]))*(1-(1-conf[0])*(1-conf[1])*(1-conf[2]))
print(a)

print(conf)
numbs = [0, 1, 2]
combs = []

for x in powerset(numbs):
    if (x) :
        combs.append(list(np.array(x)))
    
    
print(combs)
baseDelay = 10000
best =[[],[]]

demoras = []
confiabilidades = []
for i in combs:
    for j in combs:
        delay = 0
        aux = 1
        for k in i:
            aux *= (1-conf[k])
            delay+=delays[k]
        x = 1-aux

        aux = 1
        for k in j:
            aux *= (1-conf[k])
            delay+=delays[k]
        y = 1-aux
        print("conf: ",x*y," delay: ", delay, " vfn 1:",i," vnf 2: ",j)
        confiabilidades.append(x*y)
        demoras.append(delay)
        if(x*y>confmin):
            
            if (baseDelay>=delay) :
                
                baseDelay = delay
                best[0] = i
                best[1] = j
print("minimo delay :", baseDelay, " vnfs ", best)


fig, ax = plt.subplots()
ax.scatter(demoras, confiabilidades)
ax.hlines(y=confmin, xmin=0, xmax=12, linewidth=2, color='r')

plt.show()