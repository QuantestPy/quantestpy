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
            msg=None) -> None:

        state_vector.assert_is_normalized(
            state_vector_subject_to_test,
            torelance,
            msg
        )
