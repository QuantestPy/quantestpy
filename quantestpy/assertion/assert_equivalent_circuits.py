import unittest
from typing import Union

from quantestpy import QuantestPyCircuit
from quantestpy.assertion.assert_equivalent_operators import \
    assert_equivalent_operators
from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.exceptions import QuantestPyError
from quantestpy.simulator.state_vector_circuit import \
    cvt_quantestpy_circuit_to_state_vector_circuit

ut_test_case = unittest.TestCase()


def assert_equivalent_circuits(
        circuit_a: Union[QuantestPyCircuit, str],
        circuit_b: Union[QuantestPyCircuit, str],
        rtol: float = 0.,
        atol: float = 1e-8,
        up_to_global_phase: bool = False,
        matrix_norm_type: Union[str, None] = None,
        msg: Union[str, None] = None):

    if matrix_norm_type is not None and matrix_norm_type not in \
        ["operator_norm_1", "operator_norm_2",
         "operator_norm_inf", "Frobenius_norm", "max_norm"]:
        raise QuantestPyError(
            "Invalid value for matrix_norm_type. "
            "One of the following should be chosen: "
            "'operator_norm_1', 'operator_norm_2', 'operator_norm_inf', "
            "'Frobenius_norm' and 'max_norm'."
        )

    if not isinstance(atol, float):
        raise QuantestPyError(
            "Type of atol must be float."
        )

    if not isinstance(rtol, float):
        raise QuantestPyError(
            "Type of rtol must be float."
        )

    quantestpy_circuit_a = cvt_input_circuit_to_quantestpy_circuit(circuit_a)
    quantestpy_circuit_b = cvt_input_circuit_to_quantestpy_circuit(circuit_b)

    state_vector_circuit_a = cvt_quantestpy_circuit_to_state_vector_circuit(
        quantestpy_circuit_a
    )
    state_vector_circuit_b = cvt_quantestpy_circuit_to_state_vector_circuit(
        quantestpy_circuit_b
    )

    whole_gates_a = state_vector_circuit_a._get_whole_gates()
    whole_gates_b = state_vector_circuit_b._get_whole_gates()

    # call operator.assert_equal
    assert_equivalent_operators(
        whole_gates_a,
        whole_gates_b,
        rtol,
        atol,
        up_to_global_phase,
        matrix_norm_type,
        msg
    )
