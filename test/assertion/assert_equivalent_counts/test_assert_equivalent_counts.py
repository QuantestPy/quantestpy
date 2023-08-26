import unittest

from quantestpy import assert_equivalent_counts
from quantestpy.exceptions import QuantestPyAssertionError


class TestAssertEquivalentCounts(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_equivalent_counts.test_assert_equivalent_counts
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s

    OK
    $
    """

    def test_exact_equivalent(self,):
        counts_a = {
            "00": 100,
            "01": 0,
            "10": 10,
            "11": 3
        }
        counts_b = {
            "00": 100,
            "01": 0,
            "10": 10,
            "11": 3
        }
        self.assertIsNone(
            assert_equivalent_counts(
                counts_a,
                counts_b,
                sigma=1.
            )
        )

    def test_approx_equivalent(self,):
        counts_a = {
            "00": 100,
            "10": 10,
            "11": 3,
            "01": 0
        }
        counts_b = {
            "00": 80,
            "01": 0,
            "10": 15,
            "11": 4
        }
        self.assertIsNone(
            assert_equivalent_counts(
                counts_a,
                counts_b
            )
        )

    def test_not_equivalent(self,):
        counts_a = {
            "00": 100,
            "10": 10,
            "11": 3,
            "01": 0
        }
        counts_b = {
            "00": 70,
            "01": 0,
            "10": 15,
            "11": 4
        }
        with self.assertRaises(QuantestPyAssertionError) as e:
            assert_equivalent_counts(
                counts_a,
                counts_b,
                sigma=1
            )
        expected_err_msg = "The values of key 00 are too different.\n" \
            "counts_a[00] = 100, counts_b[00] = 70.\n" \
            "Difference: 30\nTolerance: 18."
        self.assertEqual(e.exception.args[0], expected_err_msg)
