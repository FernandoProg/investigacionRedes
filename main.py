import numpy as np
import time
import sys

start = time.time()

def fitness():
    arrConf = np.array([])
    arrSumDelay = np.array([])
    for i in range(population.shape[0]):
        multColumn = 1
        delay = 0
        for k in range(population.shape[2]):
            mult = 1
            rows = np.where(population[i, :, k] == 1)
            for j in rows[0]:
                mult *= (1-arrConfiability[j])
                delay += arrDelay[j]
            multColumn *= (1-mult)
        arrConf = np.append(arrConf, multColumn)
        arrSumDelay = np.append(arrSumDelay, delay)
    return arrConf / arrSumDelay

def amend():
    for i in range(population.shape[0]):    # Cada cubsistema tiene que tener al menos un componente VNF
        zeroColumns = np.where(np.sum(population[i, :, :], axis=0) == 0)
        for j in zeroColumns[0]:
            population[i, np.random.randint(typeVNF, size=1)[0], j] = 1
    return None

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

net = 20                 # Tamaño de la poblacion
typeVNF = 3             # Filas de VNF
redundantVNF = 2        # Columnas de VNF
minConfiability = 0.95  # Confiabilidad esperada
arrConfiability = np.array([0.95, 0.99, 0.97])
arrDelay = np.array([0.8, 3, 2])

population = np.random.randint(2, size = (net, typeVNF, redundantVNF))  # Creacion de la poblacion
while num_ite == 0:
    amend()
    actualFitness = fitness()
    tempChild = np.copy(population)
    tempPop = np.array([], dtype=int)
    while tempPop.shape[0] < population.shape[0]*population.shape[1]*population.shape[2]:
        seleccionadouno = np.random.choice(np.arange(net), 1, p=actualFitness/np.sum(actualFitness))[0]
        while True:
            seleccionadodos = np.random.choice(np.arange(net), 1, p=actualFitness/np.sum(actualFitness))[0]
            if seleccionadodos != seleccionadouno:
                break
        cut = np.random.randint(1, redundantVNF - 1)
        tempChild[[seleccionadouno, seleccionadodos], :, :cut] = tempChild[[seleccionadodos, seleccionadouno], :, :cut]
        if tempPop.shape[0] + typeVNF*redundantVNF*2 <= population.shape[0]*population.shape[1]*population.shape[2]:
            tempPop = np.append(tempPop, tempChild[seleccionadouno])
            tempPop = np.append(tempPop, tempChild[seleccionadodos])
        else:
            if np.random.rand() < 0.5:
                tempPop = np.append(tempPop, tempChild[seleccionadouno])
            else:
                tempPop = np.append(tempPop, tempChild[seleccionadodos])
    population = tempPop
    population.reshape((net, typeVNF, redundantVNF))
    num_ite -= 1
# tiempo ejecución
end = time.time()
print('Tiempo de ejecución:', end - start,'segundos')

