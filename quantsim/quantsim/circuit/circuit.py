from numpy import matrix

from ..core.qubit import Qubit
from .component import Component
from .gate import GateComponent
from .observer import Observer
from .qubit import QubitComponent


class Circuit:
    qubits: list[QubitComponent] = []
    observers: list[Observer] = []

    # wires and gates
    components: list[Component] = []

    def add(self, component: Component):
        if isinstance(component, QubitComponent):
            self.qubits.append(component)
        elif isinstance(component, Observer):
            self.observers.append(component)
        else:
            self.components.append(component)

    def clear(self):
        self.qubits.clear()
        self.observers.clear()
        self.components.clear()

    def remove(self, component: Component):
        if component in self.components:
            self.components.remove(component)
        elif component in self.qubits and isinstance(component, QubitComponent):
            self.qubits.remove(component)
        elif component in self.observers and isinstance(component, Observer):
            self.observers.remove(component)

    def calculate(self):
        """Sets value to observables by back tracking"""
        for qubit in self.qubits:
            gates: list[GateComponent] = []
            observer: Observer | None = None

            component = qubit
            # TODO use level order traversal of nary tree instead.
            while component is not None:
                if isinstance(component, GateComponent):
                    gates.append(component)
                elif isinstance(component, Observer):
                    observer = component
                    break
                component = component.outputs[0] if component.outputs else None

            gates = gates[::-1]
            endmat: matrix = gates.pop().gate.__array__()
            for gate in gates:
                endmat *= gate.__array__()

            qubit_mat = endmat * qubit.qubit.__array__()
            qubit = Qubit(alpha=qubit_mat.item((0, 0)), beta=qubit_mat.item(1, 0))
            if observer:
                observer.end_qubit = qubit
                observer.value = qubit.observe()
