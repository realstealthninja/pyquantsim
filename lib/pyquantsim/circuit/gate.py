import numpy as np
from pyquantsim.core import Qubit
from ..gates.gate import QuantumGate
from .component import Component


class GateComponent(Component):
    """
    GateComponent Represents a gate component in a circuit
    """

    gate: QuantumGate

    def __init__(
        self,
        gate: QuantumGate,
        inputs: list[Component] | None = None,
        outputs: list[Component] | None = None,
    ) -> None:
        """
        __init__ Constructs a quantum gate for use in a circuit

        :param gate: The gate to be usedd
        :type gate: QuantumGate
        :param inputs: The components which input into this component, defaults to None
        :type inputs: list[Component] | None, optional
        :param outputs: The components which gets output from this component, defaults to None
        :type outputs: list[Component] | None, optional
        """
        super().__init__(
            inputs if inputs is not None else [], outputs if outputs is not None else []
        )
        self.gate = gate

    def __array__(self) -> np.matrix:
        """
        __array__ Converts the gate component into a matrix

        :return: The equivalent numpy matrix
        :rtype: np.matrix
        """
        return self.gate.__array__()

    def __mul__(self, rhs: QuantumGate | GateComponent | Qubit) -> np.matrix:
        """
        __mul__ Multiplies this quantum gate with another matrix-like.

        :param rhs: The other matrix-like could be a quantum gate, gate component or a qubit
        :type rhs: QuantumGate | GateComponent | Qubit
        :return: returns the new quantum state
        :rtype: np.matrix
        """
        return self.gate.__mul__(rhs)
