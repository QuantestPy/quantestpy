import unittest
from typing import Union

import numpy as np

from quantestpy import QuantestPyCircuit
from quantestpy.assertion.assert_equivalent_operators import \
    assert_equivalent_operators
from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.simulator.state_vector_circuit import \
    cvt_quantestpy_circuit_to_state_vector_circuit

ut_test_case = unittest.TestCase()


def assert_circuit_equivalent_to_operator(
        circuit: Union[QuantestPyCircuit, str],
        operator_: Union[np.ndarray, np.matrix],
        from_right_to_left_for_qubit_ids: bool = False,
        rtol: float = 0.,
        atol: float = 1e-8,
        up_to_global_phase: bool = False,
        matrix_norm_type: Union[str, None] = None,
        msg=None) -> None:

    quantestpy_circuit = cvt_input_circuit_to_quantestpy_circuit(circuit)
    state_vector_circuit = cvt_quantestpy_circuit_to_state_vector_circuit(
        quantestpy_circuit
    )

    state_vector_circuit._from_right_to_left_for_qubit_ids = \
        from_right_to_left_for_qubit_ids

    operator_from_state_vector_circuit = \
        state_vector_circuit._get_whole_gates()

    assert_equivalent_operators(
        operator_from_state_vector_circuit,
        operator_,
        rtol,
        atol,
        up_to_global_phase,
        matrix_norm_type,
        msg
    )
