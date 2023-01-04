import random
import unittest

from quantestpy import PauliCircuit
from quantestpy.simulator.exceptions import PauliCircuitError


class TestAssertIsCorrectQubitVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.simulator.pauli_circuit.test_assert_is_correct_qubit_val
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.002s

    OK
    $
    """

    def test_regular(self,):
        circ = PauliCircuit(100)
        qubit_value = [random.randint(0, 1) for _ in range(60)]
        self.assertIsNone(
            circ._assert_is_correct_qubit_val(qubit_val=qubit_value)
        )

    def test_raise_from_qubit_val_incorrect_type(self,):
        circ = PauliCircuit(100)
        qubit_value = 0
        expected_error_msg = "qubit_val must be a list."

        with self.assertRaises(PauliCircuitError) as cm:
            circ._assert_is_correct_qubit_val(qubit_val=qubit_value)

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_val_incorrect_type(self,):
        circ = PauliCircuit(100)
        qubit_value = [0., 1]
        expected_error_msg = "Values in qubit_val must be integer type."

        with self.assertRaises(PauliCircuitError) as cm:
            circ._assert_is_correct_qubit_val(qubit_val=qubit_value)

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_val_out_of_range(self,):
        circ = PauliCircuit(100)
        qubit_value = [0, 1, 2]
        expected_error_msg = "Values in qubit_val must be either 0 or 1."

        with self.assertRaises(PauliCircuitError) as cm:
            circ._assert_is_correct_qubit_val(qubit_val=qubit_value)

        self.assertEqual(cm.exception.args[0], expected_error_msg)
