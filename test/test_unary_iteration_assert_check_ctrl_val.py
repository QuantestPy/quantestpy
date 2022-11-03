import sys
import unittest
from io import StringIO

from quantestpy import FastTestCircuit
from quantestpy.unary_iteration import \
    assert_check_ctrl_val_of_all_ops_on_syst_reg


class TestUnaryIterAssertCheckCtrlVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_unary_iteration_assert_check_ctrl_val
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.070s

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

        self.captor = StringIO()
        sys.stdout = self.captor

    def tearDown(self) -> None:
        del self.ftc
        sys.stdout = sys.__stdout__

    def test_regular(self,):
        expected_out = \
            "val in select reg: 0000, ctrl val of all ops: " \
            + "[[1], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0001, ctrl val of all ops: " \
            + "[[0], [1], [0], [0], [0], [0], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0010, ctrl val of all ops: " \
            + "[[0], [0], [1], [0], [0], [0], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0011, ctrl val of all ops: " \
            + "[[0], [0], [0], [1], [0], [0], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0100, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [1], [0], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0101, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [1], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0110, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [1], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0111, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [1], [0], [0], [0]]\n" \
            + "val in select reg: 1000, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [0], [1], [0], [0]]\n" \
            + "val in select reg: 1001, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [0], [0], [1], [0]]\n" \
            + "val in select reg: 1010, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1]]\n" \
            + "val in select reg: 1011, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1]]\n" \
            + "val in select reg: 1100, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [0], [1], [0], [0]]\n" \
            + "val in select reg: 1101, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [0], [0], [1], [0]]\n" \
            + "val in select reg: 1110, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1]]\n" \
            + "val in select reg: 1111, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1]]\n"

        assert_check_ctrl_val_of_all_ops_on_syst_reg(
            circuit=self.ftc,
            select_reg=self.select_reg,
            system_reg=self.system_reg,
            ctrl_reg=self.ctrl_reg,
            ctrl_val=self.ctrl_val,
            ancilla_reg=self.ancilla_reg
        )
        self.assertEqual(self.captor.getvalue(), expected_out)

    def test_false_for_loop_over_all_possible_vals_in_select_reg(self,):
        expected_out = \
            "val in select reg: 0000, ctrl val of all ops: " \
            + "[[1], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0001, ctrl val of all ops: " \
            + "[[0], [1], [0], [0], [0], [0], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0010, ctrl val of all ops: " \
            + "[[0], [0], [1], [0], [0], [0], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0011, ctrl val of all ops: " \
            + "[[0], [0], [0], [1], [0], [0], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0100, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [1], [0], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0101, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [1], [0], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0110, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [1], [0], [0], [0], [0]]\n" \
            + "val in select reg: 0111, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [1], [0], [0], [0]]\n" \
            + "val in select reg: 1000, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [0], [1], [0], [0]]\n" \
            + "val in select reg: 1001, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [0], [0], [1], [0]]\n" \
            + "val in select reg: 1010, ctrl val of all ops: " \
            + "[[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1]]\n"

        assert_check_ctrl_val_of_all_ops_on_syst_reg(
            circuit=self.ftc,
            select_reg=self.select_reg,
            system_reg=self.system_reg,
            ctrl_reg=self.ctrl_reg,
            ctrl_val=self.ctrl_val,
            ancilla_reg=self.ancilla_reg,
            loop_over_all_possible_vals_in_select_reg=False
        )
        self.assertEqual(self.captor.getvalue(), expected_out)
