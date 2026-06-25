from mpqp import* 
from mpqp.gates import*
from mpqp.measures import BasisMeasure
from mpqp.execution import*

import math
import random
import matplotlib.pyplot as plt

def multiTOFNul(circuit : QCircuit, control_qubits):
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
    







def multiTOF(circuit : QCircuit, control_qubits : list[int], work_qubits : list[int], target : int):
    if len(work_qubits) == 0:
        assert len(control_qubits) == 2, "If no work qubits given, there must be 2 control qubits"
        circuit.add(TOF([0,1],target))
        return

    assert len(work_qubits) == len(control_qubits) -1, f"wrong number of work qubits, should be {len(control_qubits) -1}"

    qubits = control_qubits + work_qubits + [target]

    def _multiTOF(circuit : QCircuit,control_qubits : int,work_qubits : int):
        if work_qubits == 0:
            return
        
        def _mutliTOFLeft(circuit : QCircuit,depth : int, work_qubits : int):
            if depth == 0:
                return
            if depth == 1:
                circuit.add(TOF([qubits[0],qubits[1]],qubits[work_qubits+1]))
                return
            
            _mutliTOFLeft(circuit,depth-1,work_qubits)
            circuit.add(TOF([qubits[depth + work_qubits -1],qubits[depth]],qubits[depth + work_qubits]))
        
        def _mutliTOFRight(circuit : QCircuit,depth : int, work_qubits : int):
            if depth == 0:
                return
            if depth == 1:
                circuit.add(TOF([qubits[0],qubits[1]],qubits[work_qubits+1]))
                return
            
            circuit.add(TOF([qubits[depth + work_qubits -1],qubits[depth]],qubits[depth + work_qubits]))
            _mutliTOFRight(circuit,depth-1,work_qubits)

        
        _mutliTOFLeft(circuit,len(work_qubits),len(work_qubits))
        circuit.add(CNOT(work_qubits[-1],target))
        _mutliTOFRight(circuit,len(work_qubits),len(work_qubits))
        return
        
    
    return _multiTOF(circuit,control_qubits,work_qubits)
    
    
if __name__ == "__main__":
    circuit = QCircuit(11) 
    multiTOF(circuit,[0,1,2],[3,4],10)
    multiTOF(circuit,[0,1,2],[5,6],10)
    multiTOF(circuit,[0,1],[],10)
    circuit.pretty_print()