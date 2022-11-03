import unittest

import numpy as np

from quantestpy import FastTestCircuit
from quantestpy.unary_iteration import \
    _get_ctrl_val_of_all_ops_on_syst_reg_for_given_val_in_select_reg as \
    get_ctrl_val


class TestUnaryIterGetCtrlVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_unary_iteration_get_ctrl_val
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK
    $
    """

    def setUp(self) -> None:
        """
        This is the circuit in Figure 7 in arxiv:1805.03662
        """
        self.ftc = FastTestCircuit(1+4+11+4)
        self.ftc.add_gate({"name": "x", "target_qubit": [16],
                           "control_qubit": [0, 1], "control_value": [1, 0]})
        self.ftc.add_gate({"name": "x", "target_qubit": [17],
                           "control_qubit": [16, 2], "control_value": [1, 0]})
        self.ftc.add_gate({"name": "x", "target_qubit": [18],
                           "control_qubit": [17, 3], "control_value": [1, 0]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18, 4], "control_value": [1, 0]})
        # X_0
        self.ftc.add_gate({"name": "y", "target_qubit": [5],
                           "control_qubit": [19], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18], "control_value": [1]})
        # X_1
        self.ftc.add_gate({"name": "y", "target_qubit": [6],
                           "control_qubit": [19], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18, 4], "control_value": [1, 1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [18],
                           "control_qubit": [17], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18, 4], "control_value": [1, 0]})
        # X_2
        self.ftc.add_gate({"name": "y", "target_qubit": [7],
                           "control_qubit": [19], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18], "control_value": [1]})
        # X_3
        self.ftc.add_gate({"name": "y", "target_qubit": [8],
                           "control_qubit": [19], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18, 4], "control_value": [1, 1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [18],
                           "control_qubit": [17, 3], "control_value": [1, 1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [17],
                           "control_qubit": [16], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [18],
                           "control_qubit": [17, 3], "control_value": [1, 0]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18, 4], "control_value": [1, 0]})
        # X_4
        self.ftc.add_gate({"name": "y", "target_qubit": [9],
                           "control_qubit": [19], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18], "control_value": [1]})
        # X_5
        self.ftc.add_gate({"name": "y", "target_qubit": [10],
                           "control_qubit": [19], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18, 4], "control_value": [1, 1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [18],
                           "control_qubit": [17], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18, 4], "control_value": [1, 0]})
        # X_6
        self.ftc.add_gate({"name": "y", "target_qubit": [11],
                           "control_qubit": [19], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18], "control_value": [1]})
        # X_7
        self.ftc.add_gate({"name": "y", "target_qubit": [12],
                           "control_qubit": [19], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18, 4], "control_value": [1, 1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [18],
                           "control_qubit": [17, 3], "control_value": [1, 1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [17],
                           "control_qubit": [16, 2], "control_value": [1, 1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [16],
                           "control_qubit": [0], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [18],
                           "control_qubit": [16, 3], "control_value": [1, 0]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18, 4], "control_value": [1, 0]})
        # X_8
        self.ftc.add_gate({"name": "y", "target_qubit": [13],
                           "control_qubit": [19], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18], "control_value": [1]})
        # X_9
        self.ftc.add_gate({"name": "y", "target_qubit": [14],
                           "control_qubit": [19], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [19],
                           "control_qubit": [18, 4], "control_value": [1, 1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [18],
                           "control_qubit": [16], "control_value": [1]})
        # X_10
        self.ftc.add_gate({"name": "y", "target_qubit": [15],
                           "control_qubit": [18], "control_value": [1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [18],
                           "control_qubit": [16, 3], "control_value": [1, 1]})
        self.ftc.add_gate({"name": "x", "target_qubit": [16],
                           "control_qubit": [0, 1], "control_value": [1, 1]})

        self.ctrl_reg = [0]
        self.ctrl_val = [1]
        self.select_reg = [1, 2, 3, 4]
        self.system_reg = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.ancilla_reg = [16, 17, 18, 19]

    def tearDown(self) -> None:
        del self.ftc

    def test_regular(self,):
        val_in_select_reg_to_ctrl_val = {
            "0000": [[1], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]],
            "0001": [[0], [1], [0], [0], [0], [0], [0], [0], [0], [0], [0]],
            "0010": [[0], [0], [1], [0], [0], [0], [0], [0], [0], [0], [0]],
            "0011": [[0], [0], [0], [1], [0], [0], [0], [0], [0], [0], [0]],
            "0100": [[0], [0], [0], [0], [1], [0], [0], [0], [0], [0], [0]],
            "0101": [[0], [0], [0], [0], [0], [1], [0], [0], [0], [0], [0]],
            "0110": [[0], [0], [0], [0], [0], [0], [1], [0], [0], [0], [0]],
            "0111": [[0], [0], [0], [0], [0], [0], [0], [1], [0], [0], [0]],
            "1000": [[0], [0], [0], [0], [0], [0], [0], [0], [1], [0], [0]],
            "1001": [[0], [0], [0], [0], [0], [0], [0], [0], [0], [1], [0]],
            "1010": [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1]],
            "1011": [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1]],
            "1100": [[0], [0], [0], [0], [0], [0], [0], [0], [1], [0], [0]],
            "1101": [[0], [0], [0], [0], [0], [0], [0], [0], [0], [1], [0]],
            "1110": [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1]],
            "1111": [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1]]
        }
        for val_in_select_reg, expect_ctrl_val in \
                val_in_select_reg_to_ctrl_val.items():

            actual_ctrl_val = get_ctrl_val(
                val_in_select_reg=val_in_select_reg,
                ftc=self.ftc,
                select_reg=self.select_reg,
                system_reg=self.system_reg,
                ctrl_reg=self.ctrl_reg,
                ctrl_val=self.ctrl_val,
                ancilla_reg=self.ancilla_reg
            )
            self.assertTrue(np.allclose(expect_ctrl_val, actual_ctrl_val))
