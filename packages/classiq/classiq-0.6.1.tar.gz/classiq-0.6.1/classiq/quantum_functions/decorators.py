from typing import Callable

# It really should work, and the import indeed works, everything's fine, but mypy's not happy, for a weird unkown reason
from classiq.quantum_functions.quantum_function import (  # type: ignore[attr-defined]
    QuantumFunction,
)


def quantum_function(func: Callable) -> QuantumFunction:
    qf = QuantumFunction()
    qf.add_implementation(func)
    return qf
