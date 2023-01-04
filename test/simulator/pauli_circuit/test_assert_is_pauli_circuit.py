import unittest

from quantestpy import PauliCircuit
from quantestpy.simulator.exceptions import PauliCircuitError


class TestAssertIsPauliCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.simulator.pauli_circuit.test_assert_is_pauli_circuit
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        circ = PauliCircuit(100)
        self.assertIsNone(
            PauliCircuit._assert_is_pauli_circuit(circuit=circ)
        )

    def test_raise(self,):
        circ = "dummy circuit"
        expected_error_msg = \
            "circuit must be an instance of PauliCircuit class."

        with self.assertRaises(PauliCircuitError) as cm:
            PauliCircuit._assert_is_pauli_circuit(circuit=circ)

        self.assertEqual(cm.exception.args[0], expected_error_msg)
