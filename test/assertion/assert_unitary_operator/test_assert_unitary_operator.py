import traceback
import unittest

import numpy as np

from quantestpy import assert_unitary_operator
from quantestpy.exceptions import QuantestPyAssertionError


class TestAssertUnitaryOperator(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_unitary_operator.test_assert_unitary_operator
    ....
    ----------------------------------------------------------------------
    Ran 2 tests in 0.004s

    OK
    $
    """

    def test_regular(self,):
        operator_ = np.array(
            [[1., 0., 1., 0.],
             [0., 1., 0., 1.],
             [1., 0., -1., 0.],
             [0., 1., 0., -1.]]
        ) / np.sqrt(2.) * np.exp(0.4j)

        self.assertIsNone(
            assert_unitary_operator(operator_)
        )

    def test_error_msg(self,):
        operator_ = np.array(
            [[1., 0., 1., 0.],
             [0., 1., 0., 0.],
             [1., 0., -1., 0.],
             [0., 1., 0., -1.]]
        )

        try:
            self.assertIsNotNone(
                assert_unitary_operator(operator_)
            )

        except QuantestPyAssertionError as e:

            non_identity_matrix = np.array([[2., 0., 0., 0.],
                                            [0., 1., 0., 1.],
                                            [0., 0., 2., 0.],
                                            [0., 1., 0., 2.]])

            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyAssertionError: " \
                + "Operator is not unitary.\n" \
                + f"m * m^+:\n{non_identity_matrix}\n"

            actual_error_msg = \
                traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)
