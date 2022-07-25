import numpy as np
from typing import Union

from quantestpy import operator
from quantestpy import TestCircuit
from quantestpy.exceptions import QuantestPyError


def assert_equal_to_operator(
        operator_: Union[np.ndarray, np.matrix],
        qasm: str = None,
        test_circuit: TestCircuit = None,
        number_of_decimal_places: int = 5,
        check_including_global_phase: bool = True,
        msg=None) -> None:

    #
    if qasm is None and test_circuit is None:
        raise QuantestPyError(
            "Missing qasm or test circuit."
        )

    if qasm is not None and test_circuit is not None:
        raise QuantestPyError(
            "Qasm and test circuit must not both be given."
        )

    if qasm is not None:
        raise QuantestPyError(
            "Loading qasm is not yet implemented."
        )

    _ = test_circuit._get_state_vector()
    operator_from_test_circuit = test_circuit._circuit_op

    operator.assert_equal(
        operator_from_test_circuit,
        operator_,
        number_of_decimal_places,
        check_including_global_phase,
        msg)
