from typing import override
import numpy as np
from .qubit import Qubit


class Register:
    def __init__(self, qubits: list[Qubit]):
        self.qubits: list[Qubit] = qubits
        
        previous: np.ndarray = np.asarray(qubits[0])
        for i in range(1, len(qubits)):
            previous =  np.tensordot(previous, np.asarray(self.qubits[i]), axes=0)
        self.state: np.ndarray  = previous.reshape((2**len(self.qubits), 1))

    @override
    def __str__(self) -> str:
        return " + ".join(
            f"{self.state.flat[i]} |{i:0{len(self.qubits)}b}⟩\n" 
            for i in range(self.state.size)
        )

    def __array__(self) -> np.ndarray:
        return self.state



