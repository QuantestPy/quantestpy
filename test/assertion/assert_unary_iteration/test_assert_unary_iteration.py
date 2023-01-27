import sys
import unittest
from io import StringIO
from unittest.mock import patch

from quantestpy import QuantestPyCircuit, assert_unary_iteration
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError


class TestAssertUnaryIteration(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_unary_iteration.test_assert_unary_iteration
    .........
    ----------------------------------------------------------------------
    Ran 9 tests in 0.021s

    OK
    $
    """

    def test_return_none(self,):

        qc = QuantestPyCircuit(5)
        qc.add_gate({"name": "z", "control_qubit": [0], "target_qubit": [2],
                    "control_value": [1]})
        qc.add_gate({"name": "y", "control_qubit": [0, 1], "target_qubit": [3],
                    "control_value": [1, 1]})

        self.assertIsNone(
            assert_unary_iteration(
                circuit=qc,
                index_reg=[0, 1],
                system_reg=[2, 3, 4],
                input_to_output={
                    "00": "000",
                    "01": "000",
                    "10": "100",
                    "11": "110"
                }
            )
        )

    def test_return_assert_error(self,):

        qc = QuantestPyCircuit(5)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        qc.add_gate({"name": "z", "control_qubit": [2], "target_qubit": [3],
                    "control_value": [1]})
        qc.add_gate({"name": "y", "control_qubit": [2], "target_qubit": [4],
                    "control_value": [1]})
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})

        expected_error_msg = "In bitstring: 10\n" \
            + "Out bitstring expect: 10\n" \
            + "Out bitstring actual: 00"
        with self.assertRaises(QuantestPyAssertionError) as cm:
            assert_unary_iteration(
                circuit=qc,
                index_reg=[0, 1],
                system_reg=[3, 4],
                input_to_output={
                    "00": "00",
                    "01": "00",
                    "10": "10",
                    "11": "11"
                }
            )
        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_return_ancilla_error(self,):

        qc = QuantestPyCircuit(5)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        qc.add_gate({"name": "z", "control_qubit": [2], "target_qubit": [3],
                    "control_value": [1]})
        qc.add_gate({"name": "y", "control_qubit": [2], "target_qubit": [4],
                    "control_value": [1]})
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 0]})

        expected_error_msg = "In bitstring: 10\n" \
            + "Qubits [2] in ancilla reg are not back to 0 by uncomputation."
        with self.assertRaises(QuantestPyAssertionError) as cm:
            assert_unary_iteration(
                circuit=qc,
                index_reg=[0, 1],
                system_reg=[3, 4],
                input_to_output={
                    "00": "00",
                    "01": "00",
                    "10": "00",
                    "11": "11"
                },
                ancilla_reg=[2]
            )
        self.assertEqual(cm.exception.args[0], expected_error_msg)


class TestInput(unittest.TestCase):

    def test_raise_from_invalid_input_type(self,):
        qc = QuantestPyCircuit(4)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        qc.add_gate({"name": "z", "control_qubit": [], "target_qubit": [2],
                    "control_value": []})

        expected_error_msg = "Input must be a binary bitstring."

        with self.assertRaises(QuantestPyError) as cm:
            assert_unary_iteration(
                circuit=qc,
                index_reg=[0, 1],
                system_reg=[2, 3],
                input_to_output={11: "00"}
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_invalid_input_length(self,):
        qc = QuantestPyCircuit(4)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})

        expected_error_msg = "Input bitstring has an invalid length."

        with self.assertRaises(QuantestPyError) as cm:
            assert_unary_iteration(
                circuit=qc,
                index_reg=[0, 1, 3],
                system_reg=[2],
                input_to_output={"11": "0"}
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_invalid_output_type(self,):
        qc = QuantestPyCircuit(5)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})

        expected_error_msg = "Output must be a binary bitstring."

        with self.assertRaises(QuantestPyError) as cm:
            assert_unary_iteration(
                circuit=qc,
                index_reg=[0, 1],
                system_reg=[2, 3, 4],
                input_to_output={
                    "11": ("010", [0, 0, 0.5])
                }
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_invalid_output_bitstring_length(self,):
        qc = QuantestPyCircuit(5)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        qc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [3],
                    "control_value": []})

        expected_error_msg = "Output bitstring has an invalid length."

        with self.assertRaises(QuantestPyError) as cm:
            assert_unary_iteration(
                circuit=qc,
                index_reg=[0, 1],
                system_reg=[2, 4],
                input_to_output={"11": "010"}
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

        qc = QuantestPyCircuit(5)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        qc.add_gate({"name": "z", "control_qubit": [2], "target_qubit": [3],
                    "control_value": [1]})
        qc.add_gate({"name": "y", "control_qubit": [2], "target_qubit": [4],
                    "control_value": [1]})
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})

        self.assertIsNone(
            assert_unary_iteration(
                circuit=qc,
                index_reg=[0, 1],
                system_reg=[3, 4],
                input_to_output={
                    "00": "00",
                    "01": "00",
                    "10": "00",
                    "11": "10"  # error
                },
                ancilla_reg=[2],
                draw_circuit=True
            )
        )

        stdout = self.capture.getvalue()
        self.assertIsInstance(stdout, str)

        err_msg = "In bitstring: 11\nOut bitstring expect: 10\n" \
                  + "Out bitstring actual: 11"
        self.assertTrue(err_msg in stdout)

    @ patch("builtins.input", return_value="")
    def test_ancilla_error(self, input):

        qc = QuantestPyCircuit(5)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        qc.add_gate({"name": "z", "control_qubit": [2], "target_qubit": [3],
                    "control_value": [1]})
        qc.add_gate({"name": "y", "control_qubit": [2], "target_qubit": [4],
                    "control_value": [1]})
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [0, 0]})

        self.assertIsNone(
            assert_unary_iteration(
                circuit=qc,
                index_reg=[0, 1],
                system_reg=[3, 4],
                input_to_output={
                    "00": "00",
                    "01": "00",
                    "10": "00",
                    "11": "11"
                },
                ancilla_reg=[2],
                draw_circuit=True
            )
        )

        stdout = self.capture.getvalue()
        self.assertIsInstance(stdout, str)

        err_msg = "In bitstring: 11\nQubits [2] in ancilla reg"
        self.assertTrue(err_msg in stdout)
