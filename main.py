import numpy as np
import time
import sys

start = time.time()

if len(sys.argv) == 5:  # py.exe .\main.py 1 0.9 0.1 1000
    seed = int(sys.argv[1])
    prob_cruza = float(sys.argv[2])
    prob_mut = float(sys.argv[3])
    num_ite = int(sys.argv[4])
    print("semilla: ", seed)
    print("probabilidad_cruza: ", prob_cruza)
    print("probabilidad_mutación: ", prob_mut)
    print("número_iteraciones: ", num_ite)
else:
    print('Error en la entrada de los parametros')
    sys.exit(0)

np.random.seed(seed)

typeVNF = 3
redundantVNF = 4
confiability = 0.99

population = np.array(np.random.randint(2, size = (typeVNF, redundantVNF)))
print(population.shape)
while population.shape[0] < 2:
    matrix = np.random.randint(2, size = (typeVNF, redundantVNF))
    if not matrix.sum(axis = 0).all():
        continue
    population = np.append(population, matrix)
print(population)

# tiempo ejecución
end = time.time()
print('Tiempo de ejecución:', end - start,'segundos')