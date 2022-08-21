import unittest
import traceback

from quantestpy import TestCircuit
from quantestpy.exceptions import QuantestPyTestCircuitError


class TestTestCircuitAddGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_test_circuit_add_gate
    ........
    ----------------------------------------------------------------------
    Ran 8 tests in 0.009s

    OK
    $
    """

    def test_index_in_target_qubit(self,):
        test_circuit = TestCircuit(3)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "x",
                     "target_qubit": [3],
                     "control_qubit": [],
                     "control_value": []}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: Index 3" \
                + " in target_qubit out of range for test_circuit size 3.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_index_in_control_qubit(self,):
        test_circuit = TestCircuit(10)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "cx",
                     "target_qubit": [1],
                     "control_qubit": [10],
                     "control_value": [1]}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: Index 10" \
                + " in control_qubit out of range for test_circuit size 10.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_value_in_control_value(self,):
        test_circuit = TestCircuit(3)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "cx",
                     "target_qubit": [0],
                     "control_qubit": [1],
                     "control_value": [2]}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: Value 2" \
                + " in control_value is not acceptable. " \
                + "It must be either 0 or 1.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)
