import traceback
import unittest

from quantestpy import TestCircuit
from quantestpy.exceptions import QuantestPyTestCircuitError


class TestTestCircuitAddGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_test_circuit_add_gate
    ................
    ----------------------------------------------------------------------
    Ran 16 tests in 0.001s

    OK
    $
    """

    def test_all_pass(self,):
        test_circuit = TestCircuit(3)
        test_circuit.add_gate(
            {"name": "h",
                "target_qubit": [1],
                "control_qubit": [],
                "control_value": [],
                "parameter": []}
        )
        test_circuit.add_gate(
            {"name": "x",
                "target_qubit": [2],
                "control_qubit": [0, 1],
                "control_value": [1, 1],
                "parameter": []}
        )

        expected_gates = [
            {"name": "h",
                "target_qubit": [1],
                "control_qubit": [],
                "control_value": [],
                "parameter": []},
            {"name": "x",
                "target_qubit": [2],
                "control_qubit": [0, 1],
                "control_value": [1, 1],
                "parameter": []}
        ]

        actual_gates = test_circuit._gates

        self.assertEqual(expected_gates, actual_gates)

    def test_all_pass_multi_target(self,):
        test_circuit = TestCircuit(3)
        test_circuit.add_gate(
            {"name": "x",
                "target_qubit": [1, 2],
                "control_qubit": [0],
                "control_value": [1],
                "parameter": []}
        )
        test_circuit.add_gate(
            {"name": "h",
                "target_qubit": [0, 1, 2],
                "control_qubit": [],
                "control_value": [],
                "parameter": []}
        )

        expected_gates = [
            {"name": "x",
                "target_qubit": [1, 2],
                "control_qubit": [0],
                "control_value": [1],
                "parameter": []},
            {"name": "h",
                "target_qubit": [0, 1, 2],
                "control_qubit": [],
                "control_value": [],
                "parameter": []}
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
                     "control_value": [],
                     "parameter": []}
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
                     "control_value": [],
                     "parameter": []}
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
                    {"name": "x",
                     "target_qubit": [1],
                     "control_qubit": [2, 10],
                     "control_value": [1, 1],
                     "parameter": []}
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
                    {"name": "x",
                     "target_qubit": [0],
                     "control_qubit": [1.2],
                     "control_value": [1],
                     "parameter": []}
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
                    {"name": "x",
                     "target_qubit": [0],
                     "control_qubit": [1, 2],
                     "control_value": [0, 2],
                     "parameter": []}
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
                    {"name": "x",
                     "target_qubit": [0],
                     "control_qubit": [0, 2],
                     "control_value": [1., 0],
                     "parameter": []}
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
                     "control_value": [],
                     "parameter": []}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "'target_qubit' must not an empty list.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_parameter_without_param(self,):
        test_circuit = TestCircuit(1)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "x",
                     "target_qubit": [0],
                     "control_qubit": [],
                     "control_value": [],
                     "parameter": [1]}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "x gate must have " \
                + "an empty list for 'parameter'.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_parameter_with_one_param(self,):
        test_circuit = TestCircuit(1)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "p",
                     "target_qubit": [0],
                     "control_qubit": [],
                     "control_value": [],
                     "parameter": []}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "p gate must have a list containing " \
                + "exactly 1 element for 'parameter'.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_parameter_with_three_param(self,):
        test_circuit = TestCircuit(1)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "u",
                     "target_qubit": [0],
                     "control_qubit": [],
                     "control_value": [],
                     "parameter": []}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "u gate must have a list containing " \
                + "exactly 3 elements for 'parameter'.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_value_type_in_parameter(self,):
        test_circuit = TestCircuit(1)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "p",
                     "target_qubit": [0],
                     "control_qubit": [],
                     "control_value": [],
                     "parameter": ["a"]}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "Parameter(s) in p gate must be float or integer type.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_duplicate_in_target_qubit(self,):

        test_circuit = TestCircuit(5)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "x",
                     "target_qubit": [0, 0, 2],
                     "control_qubit": [4],
                     "control_value": [1],
                     "parameter": []}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "Duplicate in target_qubit is not supported.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_duplicate_in_control_qubit(self,):

        test_circuit = TestCircuit(5)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "x",
                     "target_qubit": [0],
                     "control_qubit": [1, 2, 3, 4, 4],
                     "control_value": [1, 0, 1, 0, 1],
                     "parameter": []}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "Duplicate in control_qubit is not supported.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_intersection_in_target_and_control_qubits(self,):

        test_circuit = TestCircuit(5)

        try:
            self.assertIsNotNone(
                test_circuit.add_gate(
                    {"name": "x",
                     "target_qubit": [0, 1, 2, 3],
                     "control_qubit": [3, 4],
                     "control_value": [1, 0],
                     "parameter": []}
                )
            )

        except QuantestPyTestCircuitError as e:
            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyTestCircuitError: " \
                + "target_qubit [0, 1, 2, 3] and control_qubit [3, 4] have " \
                + "intersection.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)
