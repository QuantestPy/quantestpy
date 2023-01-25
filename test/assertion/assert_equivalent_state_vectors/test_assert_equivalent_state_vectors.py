import traceback
import unittest

import numpy as np

from quantestpy import assert_equivalent_state_vectors
from quantestpy.exceptions import QuantestPyAssertionError


class TestAssertEquivalentStateVectors(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_equivalent_state_vectors.test_assert_equivalent_state_vectors
    .....
    ----------------------------------------------------------------------
    Ran 5 tests in 0.009s

    OK
    $
    """

    def test_global_phase_calculation_1(self,):
        vec_a = np.array([1, 0, 0, 1]) / np.sqrt(2.)
        vec_b = - np.array([1, 0, 0, 1]) / np.sqrt(2.)

        self.assertIsNone(
            assert_equivalent_state_vectors(
                vec_a,
                vec_b,
                up_to_global_phase=True
            )
        )

    def test_global_phase_calculation_2(self,):
        vec_a = np.array([0.1+0.02j, 0.01, 0.5+0.007j, 0.001+0.1j]) \
            / 0.5201442107723587
        vec_b = np.array([0.1+0.02j, 0.01, 0.5+0.007j, 0.001+0.1j]) \
            / 0.5201442107723587 * np.exp(0.4j)

        self.assertIsNone(
            assert_equivalent_state_vectors(
                vec_a,
                vec_b,
                up_to_global_phase=True
            )
        )

    def test_up_to_global_phase_is_false(self,):
        vec_a = np.array([1, 1j, -1j, -0.999123j]) / 2.
        vec_b = np.array([1, 1j, -1j, -0.999j]) / 2.

        self.assertIsNone(
            assert_equivalent_state_vectors(
                vec_a,
                vec_b,
                atol=6.2e-05
            )
        )

        with self.assertRaises(QuantestPyAssertionError):
            assert_equivalent_state_vectors(
                vec_a,
                vec_b
            )

    def test_up_to_global_phase_is_false_error_on_purpose(self,):
        vec_a = np.array([0.1+0.04j, 0.01, 0.5+0.007j, 0.001+0.1j]) \
            / 0.5201442107723587
        vec_b = np.array([0.1+0.04j, 0.01, 0.5+0.007j, 0.001+0.1j]) \
            / 0.5201442107723587 * np.exp(0.4j)

        with self.assertRaises(QuantestPyAssertionError):
            assert_equivalent_state_vectors(
                vec_a,
                vec_b
            )

    def test_err_msg(self,):
        vec_a = np.array([1, 0, 0, 1]) / np.sqrt(2.)
        vec_b = - np.array([1, 0, 0, 1]) / np.sqrt(2.)

        try:
            self.assertIsNotNone(
                assert_equivalent_state_vectors(
                    vec_a,
                    vec_b,
                    rtol=1e-06,
                    atol=1e-09
                )
            )

        except QuantestPyAssertionError as e:

            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyAssertionError: \n" \
                + "Not equal to tolerance rtol=1e-06, atol=1e-09\n" \
                + "Up to global phase: False\n" \
                + "Mismatched elements: 2 / 4 (50%)\n" \
                + "Max absolute difference: 1.41421356\n" \
                + "Max relative difference: 2.\n" \
                + " x: array([0.707107, 0.      , 0.      , 0.707107])\n" \
                + " y: array([-0.707107,  0.      ,  0.      , -0.707107])\n"

            actual_error_msg = \
                traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)
