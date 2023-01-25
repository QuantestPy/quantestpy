import sys
import unittest
from io import StringIO
from unittest.mock import patch

from quantestpy import (QuantestPyCircuit,
                        assert_circuit_equivalent_to_output_qubit_state)
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError


class TestAssertEquivalent(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_circuit_equivalent_to_output_qubit_state.test_assert_circuit_equivalent_to_output_qubit_state
    .......
    ----------------------------------------------------------------------
    Ran 7 tests in 0.010s
    OK
    $
    """

    def test_return_none(self,):

        qc = QuantestPyCircuit(4)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        qc.add_gate({"name": "y", "control_qubit": [0, 2], "target_qubit": [3],
                    "control_value": [1, 1]})

        for draw_circuit in [True, False]:
            self.assertIsNone(
                assert_circuit_equivalent_to_output_qubit_state(
                    circuit=qc,
                    input_reg=[0, 1],
                    output_reg=[2, 3],
                    input_to_output={
                        "00": "00",
                        "01": "00",
                        "10": "00",
                        "11": "11"
                    },
                    draw_circuit=draw_circuit
                )
            )

    def test_return_assert_error(self,):

        qc = QuantestPyCircuit(4)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        qc.add_gate({"name": "y", "control_qubit": [0, 2], "target_qubit": [3],
                    "control_value": [1, 0]})

        expected_error_msg = "In bitstring: 10\n" \
            + "Out bitstring expect: 00\n" \
            + "Out bitstring actual: 01"

        with self.assertRaises(QuantestPyAssertionError) as cm:
            assert_circuit_equivalent_to_output_qubit_state(
                circuit=qc,
                input_reg=[0, 1],
                output_reg=[2, 3],
                input_to_output={
                    "00": "00",
                    "01": "00",
                    "10": "00",
                    "11": "11"
                }
            )
        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_invalid_input_type(self,):
        qc = QuantestPyCircuit(4)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        qc.add_gate({"name": "z", "control_qubit": [], "target_qubit": [2],
                    "control_value": []})
        qc.add_gate({"name": "y", "control_qubit": [0, 2], "target_qubit": [3],
                    "control_value": [1, 0]})

        expected_error_msg = "Input must be a binary bitstring."

        with self.assertRaises(QuantestPyError) as cm:
            assert_circuit_equivalent_to_output_qubit_state(
                circuit=qc,
                input_reg=[0, 1],
                output_reg=[2, 3],
                input_to_output={11: "00"}
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_invalid_input_length(self,):
        qc = QuantestPyCircuit(4)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})

        expected_error_msg = "Input bitstring has an invalid length."

        with self.assertRaises(QuantestPyError) as cm:
            assert_circuit_equivalent_to_output_qubit_state(
                circuit=qc,
                input_reg=[0, 1, 3],
                output_reg=[2],
                input_to_output={"11": "0"}
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_invalid_output_type(self,):
        qc = QuantestPyCircuit(4)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})

        expected_error_msg = \
            "Output must be either a binary bitstring or a tuple having " \
            + "both a binary bitstring and a list of qubit phases."

        with self.assertRaises(QuantestPyError) as cm:
            assert_circuit_equivalent_to_output_qubit_state(
                circuit=qc,
                input_reg=[0, 1, 3],
                output_reg=[2],
                input_to_output={
                    "111": ["1", [0.5]]
                }
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_invalid_output_bitstring_length(self,):
        qc = QuantestPyCircuit(4)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        qc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [3],
                    "control_value": []})

        expected_error_msg = "Output bitstring has an invalid length."

        with self.assertRaises(QuantestPyError) as cm:
            assert_circuit_equivalent_to_output_qubit_state(
                circuit=qc,
                input_reg=[0, 1],
                output_reg=[2, 3],
                input_to_output={"11": "1"}
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)


class TestDrawCircuitOption(unittest.TestCase):

    def setUp(self):
        self.capture = StringIO()
        sys.stdout = self.capture

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @ patch("builtins.input", return_value="")
    def test_assert_error(self, input):

        qc = QuantestPyCircuit(4)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        qc.add_gate({"name": "y", "control_qubit": [0, 2], "target_qubit": [3],
                    "control_value": [1, 0]})

        self.assertIsNone(
            assert_circuit_equivalent_to_output_qubit_state(
                circuit=qc,
                input_reg=[0, 1],
                output_reg=[2, 3],
                input_to_output={
                    "00": "00",
                    "01": "00",
                    "10": "00",  # error
                    "11": "11"  # error
                },
                draw_circuit=True
            )
        )

        stdout = self.capture.getvalue()
        self.assertIsInstance(stdout, str)

        for i in ["In bitstring: 10", "In bitstring: 11"]:
            self.assertTrue(i in stdout)
