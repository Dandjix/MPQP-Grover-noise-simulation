from mpqp import* 
from mpqp.gates import*
from mpqp.measures import BasisMeasure
from mpqp.execution import*

import math
import random
import matplotlib.pyplot as plt

def multiTOF(circuit : QCircuit, control_qubits):
    if control_qubits == 1:
        circuit.add(TOF([0,1],2))
        return


    def _multiTOF(circuit : QCircuit,control_qubits : int,work_qubits : int):
        if work_qubits == 0:
            return
        
        def _mutliTOFLeft(circuit : QCircuit,depth : int, work_qubits : int):
            if depth == 0:
                return
            if depth == 1:
                circuit.add(TOF([0,1],work_qubits+1))
                return
            
            _mutliTOFLeft(circuit,depth-1,work_qubits)
            circuit.add(TOF([depth + work_qubits -1,depth],depth + work_qubits))
        
        def _mutliTOFRight(circuit : QCircuit,depth : int, work_qubits : int):
            if depth == 0:
                return
            if depth == 1:
                circuit.add(TOF([0,1],work_qubits+1))
                return
            
            circuit.add(TOF([depth + work_qubits -1,depth],depth + work_qubits))
            _mutliTOFRight(circuit,depth-1,work_qubits)

        
        _mutliTOFLeft(circuit,work_qubits,work_qubits)
        circuit.add(CNOT(control_qubits + work_qubits -1,control_qubits + work_qubits))
        _mutliTOFRight(circuit,work_qubits,work_qubits)
        return
    
    return _multiTOF(circuit,control_qubits,control_qubits-1)
    
    
if __name__ == "__main__":
    circuit = QCircuit(10) # il faut un circuit deux fois plus grand que le nombre de bits dans 

    multiTOF(circuit,5)

    circuit.pretty_print()