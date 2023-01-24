import sys
import unittest
from io import StringIO
from unittest.mock import patch

from quantestpy import PauliCircuit
from quantestpy.assertion.assert_circuit_equivalent_to_output_qubit_state \
    import _draw_circuit


class TestDrawCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_circuit_equivalent_to_output_qubit_state.test_draw_circuit
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.003s

    OK
    $
    """

    def setUp(self):
        self.capture = StringIO()
        sys.stdout = self.capture

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch("builtins.input", return_value="")
    def test_regular(self, input):
        pc = PauliCircuit(5)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        pc.add_gate({"name": "z", "control_qubit": [0, 2], "target_qubit": [3],
                    "control_value": [1, 0]})

        _draw_circuit(
            pauli_circuit_org=pc,
            input_reg=[0, 1],
            output_reg=[2, 3],
            in_bitstring="11",
            err_msg="This is an err message",
            val_err_reg=[0],
            color_phase=False,
            phase_err_reg=[]

        )

        stdout = self.capture.getvalue()
        self.assertIsInstance(stdout, str)
        self.assertTrue("This is an err message" in stdout)
