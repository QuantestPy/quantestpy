import unittest
import numpy as np
from typing import Union
from quantestpy import state_vector


class QuantestPyTestCase(unittest.TestCase):
    """Add custom assertion methods
    """

    def assert_is_normalized(
            self,
            state_vector_subject_to_test: Union[np.ndarray, list],
            torelance: int = 5,
            msg=None):

        state_vector.assert_is_normalized(
            state_vector_subject_to_test,
            torelance,
            msg
        )

    def assert_equal(
            self,
            state_vector_subject_to_test: Union[np.ndarray, list],
            state_vector_expected: Union[np.ndarray, list],
            absolute_torelance_decimals: int = 8,
            determine_torelance_from_state_vector_expected: bool = False,
            msg=None):

        state_vector.assert_equal(
            state_vector_subject_to_test,
            state_vector_expected,
            absolute_torelance_decimals,
            determine_torelance_from_state_vector_expected,
            msg
        )
