from mpqp import* 
from mpqp.gates import*
from mpqp.measures import BasisMeasure
from mpqp.execution import*

import math
import random
import matplotlib.pyplot as plt
from multiTOF import multiTOF

class AncilliaryDispenser():

    input_qubits : int
    nb_anciliary : int
    given : int

    def __init__(self, input_qubits : int, nb_anciliary : int):
        self.input_qubits = input_qubits
        self.nb_anciliary = nb_anciliary
        self.given = 0

    def dispense(self,n : int):
        start = self.input_qubits + self.given
        end = start + n

        assert end < self.input_qubits + self.nb_anciliary, "No anciliary qubits left :("

        self.given += n

        return [i for i in range(start,end)]


def add_diffusion(circuit : QCircuit, n : int, dispenser : AncilliaryDispenser):
    circuit.add(Barrier())
    circuit.add([H(i) for i in range(n)])
    circuit.add(Barrier())

    circuit.add([X(i) for i in range(n)])

    circuit.add(H(2))
    control = [i for i in range(n-1)]
    nb_working = 0 if len(control) == 2  else len(control) -1
    multiTOF(circuit,control,dispenser.dispense(nb_working),n-1)
    circuit.add(H(2))

    circuit.add([X(i) for i in range(n)])

    circuit.add(Barrier())
    circuit.add([H(i) for i in range(n)])
    circuit.add(Barrier())



def add_oracle(circuit : QCircuit,n : int,searching : list, dispenser : AncilliaryDispenser):
    circuit.add(Barrier())
    for i,q in enumerate(searching):
        if(q == 0):
            circuit.add(X(i))
    circuit.add(Barrier())

    circuit.add(H(2))

    control = [i for i in range(n-1)]
    nb_working = 0 if len(control) == 2  else len(control) -1
    multiTOF(circuit,control,dispenser.dispense(nb_working),n-1)
    circuit.add(H(2))
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
    anciliary = 13

    #data structure to keep track of used anciliaries
    dispenser = AncilliaryDispenser(n,anciliary)

    #circuit init
    circuit = QCircuit(n + anciliary)
    circuit.add([H(i) for i in range(3)])


    for i in range(nb_reps):
        add_oracle(circuit,n,searching,dispenser)

        add_diffusion(circuit,n,dispenser)

    circuit.add(BasisMeasure([i for i in range(n)]))

    # circuit.pretty_print()
    result = run(circuit,IBMDevice.AER_SIMULATOR)
    result.plot()