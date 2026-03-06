from abc import ABC, abstractmethod


class Component(ABC):
    """A Base class representing a component in a quantum circuit"""

    inputs: list[Component] | None
    outputs: list[Component] | None
    id: str = ""

    def __init__(self, inputs: list[Component] | None, outputs: list[Component] | None):
        self.inputs = inputs
        self.outputs = outputs

    def connect_input(self, input: Component):
        assert self.inputs is not None
        assert input.outputs is not None

        self.inputs.append(input)
        input.outputs.append(self)

    def connect_ouput(self, output: Component):
        assert self.outputs is not None
        assert output.inputs is not None

        self.outputs.append(output)
        output.inputs.append(self)
