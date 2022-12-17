import numpy as np
import matplotlib.pyplot as plt
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
    return arrConf / arrSumDelay, arrConf, arrSumDelay

def amend():
    for i in range(population.shape[0]):    # Cada cubsistema tiene que tener al menos un componente VNF
        zeroColumns = np.where(np.sum(population[i, :, :], axis=0) == 0)
        for j in zeroColumns[0]:
            population[i, np.random.randint(typeVNF, size=1)[0], j] = 1
    return None

if len(sys.argv) == 5:  # py.exe .\test.py 1 0.1 1000 5
    seed = int(sys.argv[1])
    prob_mut = float(sys.argv[2])
    num_ite = int(sys.argv[3])
    net = int(sys.argv[4])          # Tamaño de la poblacion
    # minConfiability = float(sys.argv[5])    # Confiabilidad esperada
    print("semilla: ", seed)
    print("probabilidad_mutación: ", prob_mut)
    print("número_iteraciones: ", num_ite)
    print("Tamaño_poblacion: ", net)
    # print("Confiabilidad_minima: ", minConfiability)
else:
    print('Error en la entrada de los parametros')
    sys.exit(0)

typeVNF = np.genfromtxt('.\VNFs.csv', delimiter=' ', usecols=(1), max_rows=1, skip_header=1, dtype=int)                 # Filas de VNF
redundantVNF = np.genfromtxt('.\VNFs.csv', delimiter=' ', usecols=(1), max_rows=1, dtype=int)                           # Columnas de VNF
arrConfiability = np.genfromtxt('.\VNFs.csv', delimiter=',', usecols=(0), max_rows=typeVNF, skip_header=3, dtype=float) # Arreglo de confiabilidades por VNF
arrDelay = np.genfromtxt('.\VNFs.csv', delimiter=',', usecols=(1), max_rows=typeVNF, skip_header=3, dtype=float)        # Arreglo de delays por VNF
resp_num_ite = num_ite
resp_seed = seed
min_array = np.array([0.975, 0.987, 0.99, 0.998])
k_components = np.array([4, 9, 14, 19, 24])
best_redundant_array = []
for redundantVNF in k_components:
    array_of_conf = []
    for minConfiability in min_array:
        best_VNF = np.inf
        seed = resp_seed
        best_delay_array = []
        while seed < 10:
            np.random.seed(seed)
            num_ite = resp_num_ite
            population = np.random.randint(2, size = (net, typeVNF, redundantVNF))  # Creacion de la poblacion
            best_component = np.full((typeVNF*redundantVNF), 0).reshape(typeVNF, redundantVNF)
            best_delay = np.inf
            best_conf = 0
            while num_ite > 0:
                amend()
                conf = fitness()[1]
                delays = fitness()[2]
                for i in range(delays.shape[0]):
                    if delays[i] < best_delay and conf[i] >= minConfiability:
                        best_component = population[i]
                        best_delay = delays[i]
                        best_conf = conf[i]
                        best_VNF = np.sum(population[i])
                actualFitness = fitness()[0]
                tempChild = np.copy(population)
                tempPop = np.array([], dtype=int)
                while tempPop.shape[0] < population.shape[0]*population.shape[1]*population.shape[2]:
                    seleccionadouno = np.random.choice(np.arange(net), 1, p=actualFitness/np.sum(actualFitness))[0]
                    while True:
                        seleccionadodos = np.random.choice(np.arange(net), 1, p=actualFitness/np.sum(actualFitness))[0]
                        if seleccionadodos != seleccionadouno:
                            break
                    cut = np.random.randint(redundantVNF)
                    tempChild[[seleccionadouno, seleccionadodos], :, :cut] = tempChild[[seleccionadodos, seleccionadouno], :, :cut]
                    if tempPop.shape[0] + typeVNF*redundantVNF*2 <= population.shape[0]*population.shape[1]*population.shape[2]:
                        if np.random.rand() < prob_mut:
                            row = np.random.randint(typeVNF)
                            col = np.random.randint(redundantVNF)
                            if tempChild[seleccionadouno, row, col] == 0:
                                tempChild[seleccionadouno, row, col] = 1
                            else:
                                tempChild[seleccionadouno, row, col] = 0
                        tempPop = np.append(tempPop, tempChild[seleccionadouno])

                        if np.random.rand() < prob_mut:
                            row = np.random.randint(typeVNF)
                            col = np.random.randint(redundantVNF)
                            if tempChild[seleccionadodos, row, col] == 0:
                                tempChild[seleccionadodos, row, col] = 1
                            else:
                                tempChild[seleccionadodos, row, col] = 0
                        tempPop = np.append(tempPop, tempChild[seleccionadodos])
                    else:
                        if np.random.rand() < 0.5:
                            if np.random.rand() < prob_mut:
                                row = np.random.randint(typeVNF)
                                col = np.random.randint(redundantVNF)
                                if tempChild[seleccionadouno, row, col] == 0:
                                    tempChild[seleccionadouno, row, col] = 1
                                else:
                                    tempChild[seleccionadouno, row, col] = 0
                            tempPop = np.append(tempPop, tempChild[seleccionadouno])
                        else:
                            if np.random.rand() < prob_mut:
                                row = np.random.randint(typeVNF)
                                col = np.random.randint(redundantVNF)
                                if tempChild[seleccionadodos, row, col] == 0:
                                    tempChild[seleccionadodos, row, col] = 1
                                else:
                                    tempChild[seleccionadodos, row, col] = 0
                            tempPop = np.append(tempPop, tempChild[seleccionadodos])
                population = tempPop
                population = population.reshape((net, typeVNF, redundantVNF))
                num_ite -= 1
            best_delay_array.append(best_delay)
            seed += 1
        print(minConfiability)
        array_of_conf.append(best_delay_array)
        best_redundant_array.append(best_VNF)
    redundantVNF += 1
best_redundant_array_reshaped = np.array(best_redundant_array).reshape(min_array.shape[0], k_components.shape[0])
print(best_redundant_array_reshaped)
fig, ax= plt.subplots()
l1, = ax.plot(k_components, best_redundant_array_reshaped[0, :], color='tab:blue')
l2, = ax.plot(k_components, best_redundant_array_reshaped[1, :], color='tab:red')
l3, = ax.plot(k_components, best_redundant_array_reshaped[2, :], color='tab:green')
l4, = ax.plot(k_components, best_redundant_array_reshaped[3, :], color='tab:cyan')
ax.legend([l1, l2, l3, l4], ['97.5%', '98.7%', '99%', '99.8%'], loc='upper left')
ax.set_xlabel('Número de componentes paralelos k')
ax.set_ylabel('Total de VNFs instanciadas')
plt.show()
# tiempo ejecución
end = time.time()
print('Tiempo de ejecución:', end - start,'segundos')