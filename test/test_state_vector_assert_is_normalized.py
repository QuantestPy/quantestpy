import unittest
import numpy as np
import traceback

from quantestpy import state_vector
from quantestpy.exceptions import QuantestPyAssertionError


class TestStateVectorAssertIsNormalized(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_state_vector_assert_is_normalized
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.003s

    OK
    $
    """

    def test_regular(self,):
        vec = np.array([-1, 0, 0, 1j]) / np.sqrt(2.)

        self.assertIsNone(
            state_vector.assert_is_normalized(vec)
        )

    def test_error_msg(self,):
        vec = [-1., 1., -1j, 1j]

        try:
            self.assertIsNotNone(
                state_vector.assert_is_normalized(vec)
            )

        except QuantestPyAssertionError as e:

            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyAssertionError: " \
                + "The state vector is not normalized.\n" \
                + f"Norm: {2.}\n"

            actual_error_msg = \
                traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)
