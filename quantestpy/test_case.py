import unittest
import numpy as np
import qiskit
from typing import Union
from quantestpy import state_vector


class QuantestPyTestCase(unittest.TestCase):
    """Add custom assertion methods
    """

    def assert_is_normalized(
            self,
            state_vector_subject_to_test: Union[
                np.ndarray,
                list,
                qiskit.quantum_info.states.statevector.Statevector],
            significant_figure: int = 5,
            msg=None):

        state_vector.assert_is_normalized(
            state_vector_subject_to_test,
            significant_figure,
            msg
        )

    def assert_equal(
            self,
            state_vector_a: Union[
                np.ndarray,
                list,
                qiskit.quantum_info.states.statevector.Statevector],
            state_vector_b: Union[
                np.ndarray,
                list,
                qiskit.quantum_info.states.statevector.Statevector],
            significant_figure: int = 5,
            msg=None):

        state_vector.assert_equal(
            state_vector_a,
            state_vector_b,
            significant_figure,
            msg
        )
