import unittest
from typing import Union

import numpy as np

from quantestpy import QuantestPyCircuit
from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError
from quantestpy.simulator.state_vector_circuit import \
    cvt_quantestpy_circuit_to_state_vector_circuit

ut_test_case = unittest.TestCase()


def assert_qubit_reset_to_zero_state(circuit: Union[QuantestPyCircuit, str],
                                     qubits: list = None,
                                     atol: float = 1e-8,
                                     msg=None) -> None:

    if not isinstance(qubits, list) and qubits is not None:
        raise QuantestPyError(
            "qubits must be a list of integer(s) as qubit's ID(s)."
        )

    quantestpy_circuit = cvt_input_circuit_to_quantestpy_circuit(circuit)
    state_vector_circuit = cvt_quantestpy_circuit_to_state_vector_circuit(
        quantestpy_circuit
    )

    state_vec = state_vector_circuit._get_state_vector()
    num_qubit = state_vector_circuit.num_qubit
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
            clipped_state_vec = np.abs(clipped_state_vec)

            if not np.all(clipped_state_vec <= atol):
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
