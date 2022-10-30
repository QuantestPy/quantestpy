import unittest

from quantestpy import FastTestCircuit
from quantestpy.exceptions import QuantestPyTestCircuitError


class TestFastTestCircuitAssertIsFastTestCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.test_fast_test_circuit_assert_is_fast_test_circuit
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        circ = FastTestCircuit(100)
        self.assertIsNone(
            FastTestCircuit._assert_is_fast_test_circuit(
                circuit=circ,
                circuit_name="test_circuit"
            )
        )

    def test_raise(self,):
        circ = "dummy circuit"
        expected_error_msg = \
            "test_circuit must be an instance of FastTestCircuit class."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            FastTestCircuit._assert_is_fast_test_circuit(
                circuit=circ,
                circuit_name="test_circuit"
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)
