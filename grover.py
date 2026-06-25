from mpqp import* 
from mpqp.gates import*
from mpqp.measures import BasisMeasure
from mpqp.execution import*

import math
import random
import matplotlib.pyplot as plt
import multiTOF


def add_diffusion(circuit : QCircuit, n : int):
    circuit.add([H(i) for i in range(n)])

    circuit.add([X(i) for i in range(n)])

    circuit.add(H(2))
    circuit.add(TOF([0,1],2))
    circuit.add(H(2))

    circuit.add([X(i) for i in range(n)])

    circuit.add([H(i) for i in range(n)])


def add_oracle(circuit : QCircuit,n : int,searching : list):
    for i,q in enumerate(searching):
        if(q == 0):
            circuit.add(X(i))

    circuit.add(H(2))
    circuit.add(TOF([0,1],2))
    circuit.add(H(2))

    for i,q in enumerate(searching):
        if(q == 0):
            circuit.add(X(i))



n = 3

searching = [0,1,1,1]
circuit = QCircuit(n*2-3)

#nombre de répétitions
reps = round(math.pi/4 * math.sqrt(8))

circuit.add([H(i) for i in range(3)])


for i in range(reps):
    add_oracle(circuit,n,searching)

    add_diffusion(circuit,n)

circuit.add(BasisMeasure([i for i in range(n)]))

circuit.pretty_print()
result = run(circuit,IBMDevice.AER_SIMULATOR)
result.plot()