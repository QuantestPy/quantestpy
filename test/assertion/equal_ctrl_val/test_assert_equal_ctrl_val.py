import sys
import unittest
from io import StringIO
from unittest.mock import patch

from quantestpy import PauliCircuit, assert_equal_ctrl_val
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError


class TestAssertEqualCtrlVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.equal_ctrl_val.test_assert_equal_ctrl_val
    .......
    ----------------------------------------------------------------------
    Ran 7 tests in 0.010s

    OK
    $
    """

    def test_return_none(self,):

        pc = PauliCircuit(4)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        pc.add_gate({"name": "y", "control_qubit": [0, 2], "target_qubit": [3],
                    "control_value": [1, 1]})

        for draw_circuit in [True, False]:
            self.assertIsNone(
                assert_equal_ctrl_val(
                    circuit=pc,
                    ctrl_reg=[0, 1],
                    tgt_reg=[2, 3],
                    val_in_ctrl_reg_to_is_gate_executed_expect={
                        "00": [0, 0],
                        "01": [0, 0],
                        "10": [0, 0],
                        "11": [1, 1]
                    },
                    draw_circuit=draw_circuit
                )
            )

    def test_return_assert_error(self,):

        pc = PauliCircuit(4)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        pc.add_gate({"name": "y", "control_qubit": [0, 2], "target_qubit": [3],
                    "control_value": [1, 0]})

        expected_error_msg = "val_in_ctrl_reg: 10\n" \
            + "is_gate_executed_expect: [0, 0]\n" \
            + "is_gate_executed_actual: [0, 1]"

        with self.assertRaises(QuantestPyAssertionError) as cm:
            assert_equal_ctrl_val(
                circuit=pc,
                ctrl_reg=[0, 1],
                tgt_reg=[2, 3],
                val_in_ctrl_reg_to_is_gate_executed_expect={
                    "00": [0, 0],
                    "01": [0, 0],
                    "10": [0, 0],
                    "11": [1, 1]
                },
                draw_circuit=False
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)


class TestAssertEqualCtrlValDrawCirc(unittest.TestCase):

    def setUp(self):
        self.capture = StringIO()
        sys.stdout = self.capture

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', return_value='')
    def test_assert_error(self, input):

        pc = PauliCircuit(4)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        pc.add_gate({"name": "y", "control_qubit": [0, 2], "target_qubit": [3],
                    "control_value": [1, 0]})

        self.assertIsNone(
            assert_equal_ctrl_val(
                circuit=pc,
                ctrl_reg=[0, 1],
                tgt_reg=[2, 3],
                val_in_ctrl_reg_to_is_gate_executed_expect={
                    "00": [0, 0],
                    "01": [0, 0],
                    "10": [0, 0],  # error
                    "11": [1, 1]  # error
                },
                draw_circuit=True
            )
        )

        stdout = self.capture.getvalue()
        self.assertIsInstance(stdout, str)

        for i in ["10", "11"]:
            self.assertTrue(i in stdout)


class TestAssertEqualCtrlValInput(unittest.TestCase):

    def test_raise_from_invalid_val_type(self,):
        pc = PauliCircuit(4)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        pc.add_gate({"name": "z", "control_qubit": [], "target_qubit": [2],
                    "control_value": []})
        pc.add_gate({"name": "y", "control_qubit": [0, 2], "target_qubit": [3],
                    "control_value": [1, 0]})

        expected_error_msg = \
            "Key in val_in_ctrl_reg_to_is_gate_executed_expect must " \
            + "be a string."

        with self.assertRaises(QuantestPyError) as cm:
            assert_equal_ctrl_val(
                circuit=pc,
                ctrl_reg=[0, 1],
                tgt_reg=[2, 3],
                val_in_ctrl_reg_to_is_gate_executed_expect={
                    11: [1, 1, 0]
                },
                draw_circuit=True
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_invalid_val_length(self,):
        pc = PauliCircuit(4)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})

        expected_error_msg = \
            "Key 11 in val_in_ctrl_reg_to_is_gate_executed_expect " \
            + "has an invalid length."

        with self.assertRaises(QuantestPyError) as cm:
            assert_equal_ctrl_val(
                circuit=pc,
                ctrl_reg=[0, 1, 3],
                val_in_ctrl_reg_to_is_gate_executed_expect={
                    "11": [1]
                },
                draw_circuit=True
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_invalid_element_type(self,):
        pc = PauliCircuit(4)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})

        expected_error_msg = \
            "Element in is_gate_executed_expect must be an integer of " \
            + "either 1 or 0, where 1 indicates that the gate is " \
            + "executed while 0 not executed."

        with self.assertRaises(QuantestPyError) as cm:
            assert_equal_ctrl_val(
                circuit=pc,
                ctrl_reg=[0, 1, 3],
                val_in_ctrl_reg_to_is_gate_executed_expect={
                    "111": [2]
                },
                draw_circuit=True
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_invalid_element_length(self,):
        pc = PauliCircuit(4)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        pc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [3],
                    "control_value": []})

        expected_error_msg = "length of is_gate_executed_expect is illegal."

        with self.assertRaises(QuantestPyError) as cm:
            assert_equal_ctrl_val(
                circuit=pc,
                ctrl_reg=[0, 1],
                val_in_ctrl_reg_to_is_gate_executed_expect={
                    "11": [1]
                },
                draw_circuit=True
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)
