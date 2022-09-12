import unittest
import numpy as np

from quantestpy import operator
from quantestpy.exceptions import QuantestPyAssertionError


class TestOperatorAssertEqual(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_operator_assert_equal
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.007s

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
            operator.assert_equal(
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
            operator.assert_equal(
                op_a,
                op_b
            )
