import unittest
import numpy as np
from typing import Union
from qiskit import QuantumCircuit

from quantestpy import operator
from quantestpy import TestCircuit
from quantestpy.exceptions import QuantestPyError, QuantestPyAssertionError
from quantestpy.converter import _cvt_qiskit_to_test_circuit, _cvt_openqasm_to_test_circuit


ut_test_case = unittest.TestCase()


def assert_equal_to_operator(
        operator_: Union[np.ndarray, np.matrix],
        qasm: str = None,
        qiskit_circuit: QuantumCircuit = None,
        test_circuit: TestCircuit = None,
        from_right_to_left_for_qubit_ids: bool = False,
        number_of_decimal_places: int = 5,
        check_including_global_phase: bool = True,
        msg=None) -> None:

    if qasm is None and qiskit_circuit is None and test_circuit is None:
        raise QuantestPyError(
            "Missing qasm or qiskit_circuit or test circuit."
        )

    if (qasm is not None and qiskit_circuit is not None) \
            or (qasm is not None and test_circuit is not None) \
            or (qiskit_circuit is not None and test_circuit is not None):
        raise QuantestPyError(
            "You need to choose one parameter of Qasm, qiskit_circuit and test circuit."
        )

    if qasm is not None:
        test_circuit = _cvt_openqasm_to_test_circuit(qasm)

    if qiskit_circuit is not None:
        test_circuit = _cvt_qiskit_to_test_circuit(qiskit_circuit)

    test_circuit._from_right_to_left_for_qubit_ids = \
        from_right_to_left_for_qubit_ids

    operator_from_test_circuit = test_circuit._get_whole_gates()

    operator.assert_equal(
        operator_from_test_circuit,
        operator_,
        number_of_decimal_places,
        check_including_global_phase,
        msg)


def assert_is_zero(qasm: str = None,
                   qiskit_circuit: QuantumCircuit = None,
                   test_circuit: TestCircuit = None,
                   qubits: list = None,
                   number_of_decimal_places: int = 5,
                   msg=None) -> None:

    # Memo220805JN: the following input checker may be common for the other
    # functions in this module, thus can be one function.
    if qasm is None and qiskit_circuit is None and test_circuit is None:
        raise QuantestPyError(
            "Missing qasm or qiskit_circuit or test circuit."
        )

    if (qasm is not None and qiskit_circuit is not None) \
            or (qasm is not None and test_circuit is not None) \
            or (qiskit_circuit is not None and test_circuit is not None):
        raise QuantestPyError(
            "You need to choose one parameter of Qasm, qiskit_circuit and test circuit."
        )

    if qasm is not None:
        test_circuit = _cvt_openqasm_to_test_circuit(qasm)

    if qiskit_circuit is not None:
        test_circuit = _cvt_qiskit_to_test_circuit(qiskit_circuit)

    if not isinstance(qubits, list) and qubits is not None:
        raise QuantestPyError(
            "qubits must be a list of integer(s) as qubit's ID(s)."
        )

    state_vec = test_circuit._get_state_vector()
    num_qubit = test_circuit._num_qubit
    if qubits is None:
        qubits = [i for i in range(num_qubit)]

    def _assert_is_zero_for_one_qubit(qubit: int) -> bool:

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
                return True  # = assertion error

        return False  # = assertion non-error

    error_qubits = []
    for qubit in qubits:
        if _assert_is_zero_for_one_qubit(qubit):
            error_qubits.append(qubit)

    if len(error_qubits) > 0:
        error_msg = f"qubit(s) {error_qubits} are either non-zero or " \
            + "entangled with other qubits."
        msg = ut_test_case._formatMessage(msg, error_msg)
        raise QuantestPyAssertionError(msg)
