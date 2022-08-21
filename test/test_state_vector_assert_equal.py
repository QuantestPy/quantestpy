import unittest
import numpy as np

from quantestpy import state_vector


class TestStateVectorAssertEqual(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_state_vector_assert_equal
    ........
    ----------------------------------------------------------------------
    Ran 8 tests in 0.009s

    OK
    $
    """

    def test_global_phase_calculation_1(self,):
        vec_a = np.array([1, 0, 0, 1]) / np.sqrt(2.)
        vec_b = - np.array([1, 0, 0, 1]) / np.sqrt(2.)

        self.assertIsNone(
            state_vector.assert_equal(
                vec_a,
                vec_b,
                check_including_global_phase=False
            )
        )

    def test_global_phase_calculation_2(self,):
        vec_a = np.array([0.1+0.02j, 0.01, 0.5+0.007j, 0.001+0.1j]) \
            / 0.5201442107723587
        vec_b = np.array([0.1+0.02j, 0.01, 0.5+0.007j, 0.001+0.1j]) \
            / 0.5201442107723587 * np.exp(0.4j)

        self.assertIsNone(
            state_vector.assert_equal(
                vec_a,
                vec_b,
                check_including_global_phase=False
            )
        )
