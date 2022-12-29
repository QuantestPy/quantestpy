import sys
import unittest
from io import StringIO
from unittest.mock import patch

from quantestpy import PauliCircuit, assert_color_ctrl_val
from quantestpy.exceptions import QuantestPyError


class TestAssertColorCtrlVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.color_ctrl_val.test_assert_color_ctrl_val
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.006s

    OK
    $
    """

    def setUp(self):
        self.capture = StringIO()
        sys.stdout = self.capture

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch('builtins.input', return_value='')
    def test_regular(self, input):
        pc = PauliCircuit(3)
        pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                     "control_value": [1]})

        self.assertIsNone(
            assert_color_ctrl_val(
                circuit=pc,
                ctrl_reg=[0, 1]
            )
        )

        stdout = self.capture.getvalue()
        self.assertIsInstance(stdout, str)

        for i in ["00", "01", "10", "11"]:
            self.assertTrue(i in stdout)

    @patch('builtins.input', return_value='')
    def test_limited_inputs(self, input):
        pc = PauliCircuit(4)
        pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                     "control_value": [1]})
        pc.add_gate({"name": "swap", "control_qubit": [],
                     "target_qubit": [1, 3], "control_value": []})

        self.assertIsNone(
            assert_color_ctrl_val(
                circuit=pc,
                ctrl_reg=[0, 1],
                val_in_ctrl_reg_list=["11", "10"]
            )
        )

        stdout = self.capture.getvalue()
        self.assertIsInstance(stdout, str)

        for i in ["10", "11"]:
            self.assertTrue(i in stdout)

        for i in ["00", "01"]:
            self.assertFalse(i in stdout)

    @patch('builtins.input', return_value='')
    def test_qiskit_convention(self, input):
        pc = PauliCircuit(3)
        pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                     "control_value": [1]})

        self.assertIsNone(
            assert_color_ctrl_val(
                circuit=pc,
                ctrl_reg=[0, 1],
                from_right_to_left_for_qubit_ids=True
            )
        )

        stdout = self.capture.getvalue()
        self.assertIsInstance(stdout, str)

        for i in ["00", "01", "10", "11"]:
            self.assertTrue(i in stdout)


class TestAssertColorCtrlValInput(unittest.TestCase):

    def test_raise_from_invalid_val_type(self,):
        pc = PauliCircuit(4)
        pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                     "control_value": [1]})
        expected_error_msg = \
            "Elements in val_in_ctrl_reg_list must be strings."

        with self.assertRaises(QuantestPyError) as cm:
            assert_color_ctrl_val(
                circuit=pc,
                ctrl_reg=[0, 1, 2],
                val_in_ctrl_reg_list=[111, 101, "001"]
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)

    def test_raise_from_invalid_val_length(self,):
        pc = PauliCircuit(4)
        pc.add_gate({"name": "x", "control_qubit": [0, 2], "target_qubit": [1],
                     "control_value": [1, 0]})
        expected_error_msg = \
            "Element 01 in val_in_ctrl_reg_list has an invalid length."

        with self.assertRaises(QuantestPyError) as cm:
            assert_color_ctrl_val(
                circuit=pc,
                ctrl_reg=[0, 1, 2],
                val_in_ctrl_reg_list=["111", "01", "11"]
            )

        self.assertEqual(cm.exception.args[0], expected_error_msg)
