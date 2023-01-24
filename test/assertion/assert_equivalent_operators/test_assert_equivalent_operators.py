import traceback
import unittest

import numpy as np

from quantestpy import assert_equivalent_operators
from quantestpy.exceptions import QuantestPyAssertionError


class TestAssertEquivalentOperators(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_equivalent_operators.test_assert_equivalent_operators
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.012s

    OK
    $
    """

    def test_reqular(self,):
        op_a = np.array(
            [[1., 0., 1., 0.],
             [0., 1., 0., 1.],
             [1., 0., -1., 0.],
             [0., 1., 0., -1.]]
        ) / np.sqrt(2.)

        op_b = np.array(
            [[1., 0., 1., 0.],
             [0., 1., 0., 1.],
             [1., 0., -1., 0.],
             [0., 1., 0., -1.]]
        ) / np.sqrt(2.) * np.exp(0.4j)

        self.assertIsNone(
            assert_equivalent_operators(
                op_a,
                op_b,
                up_to_global_phase=True
            )
        )

    def test_fail_if_not_tp_to_global_phase(self,):
        op_a = np.array(
            [[1., 0., 1., 0.],
             [0., 1., 0., 1j],
             [1., 0., -1., 0.],
             [0., 1j, 0., -1.]]
        ) / np.sqrt(2.)

        op_b = np.array(
            [[1., 0., 1., 0.],
             [0., 1., 0., 1j],
             [1., 0., -1., 0.],
             [0., 1j, 0., -1.]]
        ) / np.sqrt(2.) * np.exp(0.7j)

        with self.assertRaises(QuantestPyAssertionError):
            assert_equivalent_operators(
                op_a,
                op_b
            )

    def test_matrix_norms(self,):
        op_a = np.array(
            [[0, 0, 0, 1],
             [0, 0, 1j, 0],
             [0, 1, 0, 0],
             [1j, 0, 0, 0]]
        )

        op_b = np.array(
            [[0., 0, 0, 1],
             [0, 0, 1, 0],
             [0, 1, 0, 0],
             [1, 0, 0, 0]]
        )

        test_patterns = [
            {"matrix_norm_type": "operator_norm_1",
             "atol": 1.,
             "expected_matrix_norm_value": np.sqrt(2.)},
            {"matrix_norm_type": "operator_norm_2",
             "atol": 1.,
             "expected_matrix_norm_value": np.sqrt(2.)},
            {"matrix_norm_type": "operator_norm_inf",
             "atol": 1.4,
             "expected_matrix_norm_value": np.sqrt(2.)},
            {"matrix_norm_type": "Frobenius_norm",
             "atol": 1.9,
             "expected_matrix_norm_value": 2.},
            {"matrix_norm_type": "max_norm",
             "atol": 0.1,
             "expected_matrix_norm_value": np.sqrt(2.)}
        ]

        for pattern in test_patterns:

            try:
                self.assertIsNotNone(
                    assert_equivalent_operators(
                        operator_a=op_a,
                        operator_b=op_b,
                        matrix_norm_type=pattern["matrix_norm_type"],
                        atol=pattern["atol"]
                    )
                )

            except QuantestPyAssertionError as e:

                expected_error_msg = \
                    "quantestpy.exceptions.QuantestPyAssertionError: " \
                    + "matrix norm ||A-B|| " \
                    + format(pattern["expected_matrix_norm_value"], ".15g") \
                    + " is larger than (atol + rtol*||B||) " \
                    + format(pattern["atol"], ".15g") \
                    + "."

                actual_error_msg = \
                    traceback.format_exception_only(type(e), e)[0].rstrip("\n")

                self.assertEqual(expected_error_msg, actual_error_msg)
