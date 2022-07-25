import unittest
import numpy as np
from typing import Union

from quantestpy import state_vector, operator


class QuantestPyTestCase(unittest.TestCase):
    """Add custom assertion methods
    """

    def state_vector_assert_is_normalized(
            self,
            state_vector_subject_to_test: Union[np.ndarray, list],
            number_of_decimal_places: int = 5,
            msg=None):

        state_vector.assert_is_normalized(
            state_vector_subject_to_test,
            number_of_decimal_places,
            msg
        )

    def state_vector_assert_equal(
            self,
            state_vector_a: Union[np.ndarray, list],
            state_vector_b: Union[np.ndarray, list],
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
            operator_subject_to_test: Union[np.ndarray, np.matrix],
            number_of_decimal_places: int = 5,
            msg=None):

        operator.assert_is_unitary(
            operator_subject_to_test,
            number_of_decimal_places,
            msg
        )

    def operator_assert_equal(
            self,
            operator_a: Union[np.ndarray, np.matrix],
            operator_b: Union[np.ndarray, np.matrix],
            number_of_decimal_places: int = 5,
            check_including_global_phase: bool = True,
            msg=None):

        operator.assert_equal(
            operator_a,
            operator_b,
            number_of_decimal_places,
            check_including_global_phase,
            msg
        )
