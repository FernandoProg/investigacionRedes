import numpy as np
import time
import sys

start = time.time()

if len(sys.argv) == 7:
    seed = int(sys.argv[1])
    tamaño_tabl = int(sys.argv[2])
    
    tamaño_pobl = int(sys.argv[3])
    prob_cruza = float(sys.argv[4])
    prob_mut = float(sys.argv[5])
    num_ite = int(sys.argv[6])
    print("semilla: ", seed)
    print("tamaño_tablero: ", tamaño_tabl)
    print("tamaño_población: ", tamaño_pobl)
    print("probabilidad_cruza: ", prob_cruza)
    print("probabilidad_mutación: ", prob_mut)
    print("número_iteraciones: ", num_ite)
else:
    print('Error en la entrada de los parametros')
    print('Los paramentros a ingresar son: semilla TamañoTablero TamañoPoblación ProbabilidadCruza ProbabilidadMutación NumeroIteración')
    sys.exit(0)

# tiempo ejecución
end = time.time()
print('Tiempo de ejecución:', end - start,'segundos')