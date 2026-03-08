from abc import ABC, abstractmethod


class Component(ABC):
    """
    Component Represents a component in a circuit
    """

    inputs: list[Component] | None
    outputs: list[Component] | None
    id: str = ""

    def __init__(self, inputs: list[Component] | None, outputs: list[Component] | None):
        """
        __init__ Constructor for component

        :param inputs: A list of input components that the component is connected to
        :type inputs: list[Component] | None
        :param outputs: A list of output components that the component is connect to
        :type outputs: list[Component] | None
        """
        self.inputs = inputs
        self.outputs = outputs

    def connect_input(self, input: Component):
        """
        connect_input Connects this component's input to another's output

        :param input: The input component
        :type input: Component
        """
        assert self.inputs is not None
        assert input.outputs is not None

        self.inputs.append(input)
        input.outputs.append(self)

    def connect_ouput(self, output: Component):
        """
        connect_ouput Connects this component's output to another's input

        :param output: The output component
        :type output: Component
        """
        assert self.outputs is not None
        assert output.inputs is not None

        self.outputs.append(output)
        output.inputs.append(self)
