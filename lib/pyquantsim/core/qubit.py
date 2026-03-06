import numpy as np
from numpy.random import choice

from math import sqrt
from random import random
from typing_extensions import override


class Qubit:
    observed: bool | None = None

    def __init__(
        self,
        alpha: complex | None = None,
        beta: complex | None = None,
        matrix: np.matrix | None = None,
    ) -> None:
        if matrix is not None:
            self.alpha = matrix[0][0][0]
            self.beta = matrix[1][0][0]
        elif alpha and beta:
            self.alpha = alpha
            self.beta = beta
        else:
            state: list[float] = [random() for _ in range(0, 4)]
            s = sum(state)
            state = list(map(lambda i: i / s, state))
            from random import choice

            a = sqrt(state[0]) * choice([1, -1])
            b = sqrt(state[1]) * choice([1, -1])
            c = sqrt(state[2]) * choice([1, -1])
            d = sqrt(state[3]) * choice([1, -1])

            self.alpha: complex = complex(a, b)
            self.beta: complex = complex(c, d)

    @override
    def __str__(self) -> str:
        return f"{self.alpha}|0⟩ + {self.beta}|1⟩"

    def __array__(self) -> np.typing.NDArray[np.complex256]:
        return np.c_[[self.alpha, self.beta]]

    def observe(self) -> bool:
        if self.observed is not None:
            return self.observed

        alpha_sqr = self.alpha.real**2 + self.alpha.imag**2
        beta_sqr = self.beta.real**2 + self.beta.imag**2

        p = np.array([alpha_sqr, beta_sqr], dtype=np.float64)
        p = p / np.sum(p, dtype=np.float64)  # normalise
        a = np.array([False, True], dtype=bool)
        chosen: bool = bool(choice(a, p=p))
        self.observed = chosen

        return chosen
