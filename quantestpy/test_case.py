import unittest
import numpy as np
import qiskit
from typing import Union
from quantestpy import state_vector, matrix


class QuantestPyTestCase(unittest.TestCase):
    """Add custom assertion methods
    """

    def state_vector_assert_is_normalized(
            self,
            state_vector_subject_to_test: Union[
                np.ndarray,
                list,
                qiskit.quantum_info.states.statevector.Statevector],
            number_of_decimal_places: int = 5,
            msg=None):

        state_vector.assert_is_normalized(
            state_vector_subject_to_test,
            number_of_decimal_places,
            msg
        )

    def state_vector_assert_equal(
            self,
            state_vector_a: Union[
                np.ndarray,
                list,
                qiskit.quantum_info.states.statevector.Statevector],
            state_vector_b: Union[
                np.ndarray,
                list,
                qiskit.quantum_info.states.statevector.Statevector],
            number_of_decimal_places: int = 5,
            check_including_global_phase: bool = True,
            msg=None):

        state_vector.assert_equal(
            state_vector_a,
            state_vector_b,
            number_of_decimal_places,
            check_including_global_phase,
            msg
        )

    def operator_assert_is_unitary(
            self,
            matrix_subject_to_test: Union[
                np.ndarray,
                np.matrix,
                qiskit.quantum_info.operators.operator.Operator],
            number_of_decimal_places: int = 5,
            msg=None):

        matrix.assert_is_unitary(
            matrix_subject_to_test,
            number_of_decimal_places,
            msg
        )

    def operator_assert_equal(
            self,
            matrix_a: Union[
                np.ndarray,
                qiskit.quantum_info.operators.operator.Operator],
            matrix_b: Union[
                np.ndarray,
                list,
                qiskit.quantum_info.operators.operator.Operator],
            number_of_decimal_places: int = 5,
            check_including_global_phase: bool = True,
            msg=None):

        matrix.assert_equal(
            matrix_a,
            matrix_b,
            number_of_decimal_places,
            check_including_global_phase,
            msg
        )
