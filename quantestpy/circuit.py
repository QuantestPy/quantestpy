import numpy as np
from typing import Union

from quantestpy import operator
from quantestpy import TestCircuit
from quantestpy.exceptions import QuantestPyError, QuantestPyAssertionError
from quantestpy.test_circuit import cvt_openqasm_to_test_circuit


def assert_equal_to_operator(
        operator_: Union[np.ndarray, np.matrix],
        qasm: str = None,
        test_circuit: TestCircuit = None,
        from_right_to_left_for_qubit_ids: bool = None,
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
        test_circuit = cvt_openqasm_to_test_circuit(qasm)
        raise QuantestPyError(
            "Loading qasm is not yet implemented."
        )

    if from_right_to_left_for_qubit_ids is not None:
        test_circuit._from_right_to_left_for_qubit_ids = \
            from_right_to_left_for_qubit_ids

    operator_from_test_circuit = test_circuit._get_circuit_operator()

    operator.assert_equal(
        operator_from_test_circuit,
        operator_,
        number_of_decimal_places,
        check_including_global_phase,
        msg)


def assert_is_zero(qasm: str = None,
                   test_circuit: TestCircuit = None,
                   qubits: list = None,
                   number_of_decimal_places: int = 5) -> None:

    # Memo220805JN: the following input checker may be common for the other
    # functions in this module, thus can be one function.
    if qasm is None and test_circuit is None:
        raise QuantestPyError(
            "Missing qasm or test circuit."
        )

    if qasm is not None and test_circuit is not None:
        raise QuantestPyError(
            "Qasm and test circuit must not both be given."
        )

    if qasm is not None:
        test_circuit = cvt_openqasm_to_test_circuit(qasm)
        raise QuantestPyError(
            "Loading qasm is not yet implemented."
        )

    if not isinstance(qubits, list) and qubits is not None:
        raise QuantestPyError(
            "qubits must be a list of integer(s) as qubit's ID(s)."
        )

    state_vec = test_circuit._get_state_vector()
    num_qubit = test_circuit._num_qubit
    if qubits is None:
        qubits = [i for i in range(num_qubit)]

    def _assert_is_zero_for_one_qubit(qubit):

        if qubit > num_qubit-1:
            raise QuantestPyError(
                f"qubit {qubit} is out of range for the given circuit."
            )

        dim_reg_front = 2**qubit
        dim_reg_rear = 2**(num_qubit - qubit - 1)

        for i in range(dim_reg_front):
            clipped_state_vec = \
                state_vec[i*dim_reg_rear*2: (i+1)*dim_reg_rear*2]
            clipped_state_vec = clipped_state_vec[dim_reg_rear:]
            clipped_state_vec = np.round(
                clipped_state_vec, decimals=number_of_decimal_places)

            if not np.all(clipped_state_vec == 0.):
                raise QuantestPyAssertionError(
                    f"qubit {qubit} is either non-zero or "
                    "entangled with other qubits."
                )

    for qubit in qubits:
        _assert_is_zero_for_one_qubit(qubit)
