import traceback
import unittest

from quantestpy import QuantestPyCircuit
from quantestpy.simulator.exceptions import QuantestPyCircuitError


class TestQuantestPyCircuitAddGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.quantestpy_circuit.test_add_gate
    ............
    ----------------------------------------------------------------------
    Ran 12 tests in 0.001s

    OK
    $
    """

    def test_all_pass(self,):
        qc = QuantestPyCircuit(3)
        qc.add_gate(
            {"name": "h",
                "target_qubit": [1],
                "control_qubit": [],
                "control_value": [],
                "parameter": []}
        )
        qc.add_gate(
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

        actual_gates = qc._gates

        self.assertEqual(expected_gates, actual_gates)

    def test_all_pass_multi_target(self,):
        qc = QuantestPyCircuit(3)
        qc.add_gate(
            {"name": "x",
                "target_qubit": [1, 2],
                "control_qubit": [0],
                "control_value": [1],
                "parameter": []}
        )
        qc.add_gate(
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

        actual_gates = qc._gates

        self.assertEqual(expected_gates, actual_gates)

    def test_index_range_in_target_qubit(self,):
        qc = QuantestPyCircuit(3)

        try:
            self.assertIsNotNone(
                qc.add_gate(
                    {"name": "x",
                     "target_qubit": [3],
                     "control_qubit": [],
                     "control_value": [],
                     "parameter": []}
                )
            )

        except QuantestPyCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.QuantestPyCircuitError: " \
                + "Index 3" \
                + " in target_qubit out of range for circuit size 3.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_index_type_in_target_qubit(self,):
        qc = QuantestPyCircuit(4)

        try:
            self.assertIsNotNone(
                qc.add_gate(
                    {"name": "h",
                     "target_qubit": [1.],
                     "control_qubit": [],
                     "control_value": [],
                     "parameter": []}
                )
            )

        except QuantestPyCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.QuantestPyCircuitError: " \
                + "Index in target_qubit must be integer type.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_index_range_in_control_qubit(self,):
        qc = QuantestPyCircuit(10)

        try:
            self.assertIsNotNone(
                qc.add_gate(
                    {"name": "x",
                     "target_qubit": [1],
                     "control_qubit": [2, 10],
                     "control_value": [1, 1],
                     "parameter": []}
                )
            )

        except QuantestPyCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.QuantestPyCircuitError: " \
                + "Index 10" \
                + " in control_qubit out of range for circuit size 10.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_index_type_in_control_qubit(self,):
        qc = QuantestPyCircuit(3)

        try:
            self.assertIsNotNone(
                qc.add_gate(
                    {"name": "x",
                     "target_qubit": [0],
                     "control_qubit": [1.2],
                     "control_value": [1],
                     "parameter": []}
                )
            )

        except QuantestPyCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.QuantestPyCircuitError: " \
                + "Index in control_qubit must be integer type.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_value_range_in_control_value(self,):
        qc = QuantestPyCircuit(3)

        try:
            self.assertIsNotNone(
                qc.add_gate(
                    {"name": "x",
                     "target_qubit": [0],
                     "control_qubit": [1, 2],
                     "control_value": [0, 2],
                     "parameter": []}
                )
            )

        except QuantestPyCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.QuantestPyCircuitError: " \
                + "Value 2" \
                + " in control_value is not acceptable. " \
                + "It must be either 0 or 1.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_value_type_in_control_value(self,):
        qc = QuantestPyCircuit(3)

        try:
            self.assertIsNotNone(
                qc.add_gate(
                    {"name": "x",
                     "target_qubit": [0],
                     "control_qubit": [0, 2],
                     "control_value": [1., 0],
                     "parameter": []}
                )
            )

        except QuantestPyCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.QuantestPyCircuitError: " \
                + "Value in control_value must be integer type.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_target_qubit_empty(self,):
        qc = QuantestPyCircuit(5)

        try:
            self.assertIsNotNone(
                qc.add_gate(
                    {"name": "t",
                     "target_qubit": [],
                     "control_qubit": [],
                     "control_value": [],
                     "parameter": []}
                )
            )

        except QuantestPyCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.QuantestPyCircuitError: " \
                + "'target_qubit' must not an empty list.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_duplicate_in_target_qubit(self,):

        qc = QuantestPyCircuit(5)

        try:
            self.assertIsNotNone(
                qc.add_gate(
                    {"name": "x",
                     "target_qubit": [0, 0, 2],
                     "control_qubit": [4],
                     "control_value": [1],
                     "parameter": []}
                )
            )

        except QuantestPyCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.QuantestPyCircuitError: " \
                + "Duplicate in target_qubit is not supported.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_duplicate_in_control_qubit(self,):

        qc = QuantestPyCircuit(5)

        try:
            self.assertIsNotNone(
                qc.add_gate(
                    {"name": "x",
                     "target_qubit": [0],
                     "control_qubit": [1, 2, 3, 4, 4],
                     "control_value": [1, 0, 1, 0, 1],
                     "parameter": []}
                )
            )

        except QuantestPyCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.QuantestPyCircuitError: " \
                + "Duplicate in control_qubit is not supported.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_intersection_in_target_and_control_qubits(self,):

        qc = QuantestPyCircuit(5)

        try:
            self.assertIsNotNone(
                qc.add_gate(
                    {"name": "x",
                     "target_qubit": [0, 1, 2, 3],
                     "control_qubit": [3, 4],
                     "control_value": [1, 0],
                     "parameter": []}
                )
            )

        except QuantestPyCircuitError as e:
            expected_error_msg = \
                "quantestpy.simulator.exceptions.QuantestPyCircuitError: " \
                + "target_qubit [0, 1, 2, 3] and control_qubit [3, 4] have " \
                + "intersection.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)
