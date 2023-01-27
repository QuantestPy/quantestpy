import sys
import unittest
from io import StringIO
from unittest.mock import patch

from quantestpy import PauliCircuit
from quantestpy.assertion.assert_unary_iteration import _draw_circuit


class TestDrawCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_unary_iteration.test_draw_circuit
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.008s

    OK
    $
    """

    def setUp(self):
        self.capture = StringIO()
        sys.stdout = self.capture

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch("builtins.input", return_value="")
    def test_color_system_reg(self, input):
        pc = PauliCircuit(5)
        pc.add_gate({"name": "z", "control_qubit": [0], "target_qubit": [2],
                    "control_value": [1]})
        pc.add_gate({"name": "y", "control_qubit": [0, 1], "target_qubit": [3],
                    "control_value": [1, 1]})

        _draw_circuit(
            pauli_circuit_org=pc,
            index_reg=[0, 1],
            output_reg=[2, 3, 4],
            output_reg_name="system",
            in_bitstring="11",
            err_msg="This is an err msg.",
            val_err_reg=[3],
            replace_gate=True
        )

        stdout = self.capture.getvalue()
        self.assertIsInstance(stdout, str)
        for s in ["This is an err msg.", "[X]"]:
            self.assertTrue(s in stdout)

    @patch("builtins.input", return_value="")
    def test_color_ancilla_reg(self, input):
        pc = PauliCircuit(5)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        pc.add_gate({"name": "y", "control_qubit": [2], "target_qubit": [3],
                    "control_value": [1]})
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [0, 0]})

        _draw_circuit(
            pauli_circuit_org=pc,
            index_reg=[0, 1],
            output_reg=[2],
            output_reg_name="ancilla",
            in_bitstring="11",
            err_msg="This is an err msg.",
            val_err_reg=[2]
        )

        stdout = self.capture.getvalue()
        self.assertIsInstance(stdout, str)
        for s in ["This is an err msg.", "[Y]"]:
            self.assertTrue(s in stdout)
