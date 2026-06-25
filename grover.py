from mpqp import* 
from mpqp.gates import*
from mpqp.measures import BasisMeasure
from mpqp.execution import*

import math
import random
import matplotlib.pyplot as plt
from multiTOF import multiTOF


def add_diffusion(circuit : QCircuit, n : int, working_qubits : list[int]):
    circuit.add(Barrier())
    circuit.add([H(i) for i in range(n)])
    circuit.add(Barrier())

    circuit.add([X(i) for i in range(n)])

    circuit.add(H(n-1))
    multiTOF(circuit,[i for i in range(n-1)],working_qubits,n-1)
    circuit.add(H(n-1))

    circuit.add([X(i) for i in range(n)])

    circuit.add(Barrier())
    circuit.add([H(i) for i in range(n)])
    circuit.add(Barrier())



def add_oracle(circuit : QCircuit,n : int,searching : list, working_qubits : list[int]):
    circuit.add(Barrier())
    for i,q in enumerate(searching):
        if(q == 0):
            circuit.add(X(i))
    circuit.add(Barrier())

    circuit.add(H(n-1))
    multiTOF(circuit,[i for i in range(n-1)],working_qubits,n-1)
    circuit.add(H(n-1))
    circuit.add(Barrier())

    for i,q in enumerate(searching):
        if(q == 0):
            circuit.add(X(i))
    circuit.add(Barrier())

def number_anciliary_qubits(nb_reps : int, n : int):
    assert n >= 3 , "cannot apply Grover on less than 3 qubits"

    if n == 3 : return 0 #no need for extra qubits

    return (n-2) * nb_reps * 2 # *2 cuz we need a bunch for the Oracle and as many again for the diffusion



if __name__ == "__main__":
    n = 4 # number of qubits as inputs for the circuit
    domain_size = 2**n # usually noted N

    searching = [random.randint(0,1) for i in range(n)]

    assert len(searching) == n, f"should search a value of length {n}"


    #number of repetitions
    nb_reps = round(math.pi/4 * math.sqrt(domain_size))

    #number of anciliary qubits for multiTOF
    nb_anciliary = 0 if n == 3 else n-2
    anciliary = [n+i for i in range(nb_anciliary)]

    #circuit init
    circuit = QCircuit(n + nb_anciliary)
    circuit.add([H(i) for i in range(3)])


    for i in range(nb_reps):
        add_oracle(circuit,n,searching,anciliary)

        add_diffusion(circuit,n,anciliary)

    circuit.add(BasisMeasure([i for i in range(n)]))

    # circuit.pretty_print()
    result = run(circuit,IBMDevice.AER_SIMULATOR)

    result.plot()