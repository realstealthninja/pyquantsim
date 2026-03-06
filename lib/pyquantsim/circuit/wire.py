from .component import Component


class WireComponent(Component):
    def __init__(self, inputs: list[Component], outputs: list[Component]):
        super().__init__(inputs, outputs)
