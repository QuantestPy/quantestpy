import unittest

from quantestpy import PauliCircuit
from quantestpy.exceptions import QuantestPyTestCircuitError


class TestPauliCircuitAssertIsPauliCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.simulator.test_pauli_circuit_assert_is_fast_test_circuit
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        circ = PauliCircuit(100)
        self.assertIsNone(
            PauliCircuit._assert_is_pauli_circuit(
                circuit=circ,
                circuit_name="test_circuit"
            )
        )

    def test_raise(self,):
        circ = "dummy circuit"
        expected_error_msg = \
            "test_circuit must be an instance of PauliCircuit class."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            PauliCircuit._assert_is_pauli_circuit(
                circuit=circ,
                circuit_name="test_circuit"
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)
