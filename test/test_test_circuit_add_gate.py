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
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 0.003s

    OK
    $
    """

    def test_all_pass(self,):
        test_circuit = TestCircuit(3)
        test_circuit.add_gate(
            {"name": "h",
                "target_qubit": [1],
                "control_qubit": [],
                "control_value": []}
        )
        test_circuit.add_gate(
            {"name": "cx",
                "target_qubit": [2],
                "control_qubit": [0, 1],
                "control_value": [1, 1]}
        )

        expected_gates = [
            {"name": "h",
                "target_qubit": [1],
                "control_qubit": [],
                "control_value": []},
            {"name": "cx",
                "target_qubit": [2],
                "control_qubit": [0, 1],
                "control_value": [1, 1]}
        ]

        actual_gates = test_circuit._gates

        self.assertEqual(expected_gates, actual_gates)

    def test_all_pass_multi_target(self,):
        test_circuit = TestCircuit(3)
        test_circuit.add_gate(
            {"name": "cx",
                "target_qubit": [1, 2],
                "control_qubit": [0],
                "control_value": [1]}
        )
        test_circuit.add_gate(
            {"name": "h",
                "target_qubit": [0, 1, 2],
                "control_qubit": [],
                "control_value": []}
        )

        expected_gates = [
            {"name": "cx",
                "target_qubit": [1, 2],
                "control_qubit": [0],
                "control_value": [1]},
            {"name": "h",
                "target_qubit": [0, 1, 2],
                "control_qubit": [],
                "control_value": []}
        ]

        actual_gates = test_circuit._gates

        self.assertEqual(expected_gates, actual_gates)

    def test_index_range_in_target_qubit(self,):
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

    def test_index_type_in_target_qubit(self,):
        test_circuit = TestCircuit(4)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "h",
                     "target_qubit": [1.],
                     "control_qubit": [],
                     "control_value": []}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "Index in target_qubit must be integer type.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_index_range_in_control_qubit(self,):
        test_circuit = TestCircuit(10)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "cx",
                     "target_qubit": [1],
                     "control_qubit": [2, 10],
                     "control_value": [1, 1]}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: Index 10" \
                + " in control_qubit out of range for test_circuit size 10.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_index_type_in_control_qubit(self,):
        test_circuit = TestCircuit(3)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "cx",
                     "target_qubit": [0],
                     "control_qubit": [1.2],
                     "control_value": [1]}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "Index in control_qubit must be integer type.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_value_range_in_control_value(self,):
        test_circuit = TestCircuit(3)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "cx",
                     "target_qubit": [0],
                     "control_qubit": [1, 2],
                     "control_value": [0, 2]}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: Value 2" \
                + " in control_value is not acceptable. " \
                + "It must be either 0 or 1.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_value_type_in_control_value(self,):
        test_circuit = TestCircuit(3)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "cx",
                     "target_qubit": [0],
                     "control_qubit": [0, 2],
                     "control_value": [1., 0]}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "Value in control_value must be integer type.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_target_qubit_empty(self,):
        test_circuit = TestCircuit(5)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "t",
                     "target_qubit": [],
                     "control_qubit": [],
                     "control_value": []}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "'target_qubit' must not an empty list.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)
