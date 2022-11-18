import random
import unittest

from quantestpy import PauliCircuit
from quantestpy.exceptions import QuantestPyTestCircuitError


class TestPauliCircuitAssertIsCorrectQubitVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.simulator.test_pauli_circuit_assert_is_correct_qubit_val
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
            circ._assert_is_correct_qubit_val(
                qubit_val=qubit_value,
                qubit_val_name="test_qubit_value"
            )
        )

    def test_raise_from_qubit_val_incorrect_type(self,):
        circ = PauliCircuit(100)
        qubit_value = 0
        expected_error_msg = "test_qubit_value must be a list."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            circ._assert_is_correct_qubit_val(
                qubit_val=qubit_value,
                qubit_val_name="test_qubit_value"
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_val_incorrect_type(self,):
        circ = PauliCircuit(100)
        qubit_value = [0., 1]
        expected_error_msg = \
            "Values in test_qubit_value must be integer type."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            circ._assert_is_correct_qubit_val(
                qubit_val=qubit_value,
                qubit_val_name="test_qubit_value"
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_val_out_of_range(self,):
        circ = PauliCircuit(100)
        qubit_value = [0, 1, 2]
        expected_error_msg = \
            "Values in test_qubit_value must be either 0 or 1."

        with self.assertRaises(QuantestPyTestCircuitError) as cm:
            circ._assert_is_correct_qubit_val(
                qubit_val=qubit_value,
                qubit_val_name="test_qubit_value"
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)
