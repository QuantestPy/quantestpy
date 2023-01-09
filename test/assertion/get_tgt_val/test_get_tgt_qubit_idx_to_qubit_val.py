import unittest

from quantestpy import PauliCircuit
from quantestpy.assertion.get_tgt_val import \
    _get_tgt_qubit_idx_to_qubit_val_for_given_val_in_ctrl_reg as get_tgt_val


class TestGetTgtQubitIdxToQubitVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.get_tgt_val.test_get_tgt_qubit_idx_to_qubit_val
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
        self.pc = PauliCircuit(1+4+11+4)
        self.pc.add_gate({"name": "x", "target_qubit": [16],
                          "control_qubit": [0, 1], "control_value": [1, 0]})
        self.pc.add_gate({"name": "x", "target_qubit": [17],
                          "control_qubit": [16, 2], "control_value": [1, 0]})
        self.pc.add_gate({"name": "x", "target_qubit": [18],
                          "control_qubit": [17, 3], "control_value": [1, 0]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18, 4], "control_value": [1, 0]})
        # X_0
        self.pc.add_gate({"name": "y", "target_qubit": [5],
                          "control_qubit": [19], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18], "control_value": [1]})
        # X_1
        self.pc.add_gate({"name": "y", "target_qubit": [6],
                          "control_qubit": [19], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18, 4], "control_value": [1, 1]})
        self.pc.add_gate({"name": "x", "target_qubit": [18],
                          "control_qubit": [17], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18, 4], "control_value": [1, 0]})
        # X_2
        self.pc.add_gate({"name": "y", "target_qubit": [7],
                          "control_qubit": [19], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18], "control_value": [1]})
        # X_3
        self.pc.add_gate({"name": "y", "target_qubit": [8],
                          "control_qubit": [19], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18, 4], "control_value": [1, 1]})
        self.pc.add_gate({"name": "x", "target_qubit": [18],
                          "control_qubit": [17, 3], "control_value": [1, 1]})
        self.pc.add_gate({"name": "x", "target_qubit": [17],
                          "control_qubit": [16], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [18],
                          "control_qubit": [17, 3], "control_value": [1, 0]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18, 4], "control_value": [1, 0]})
        # X_4
        self.pc.add_gate({"name": "y", "target_qubit": [9],
                          "control_qubit": [19], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18], "control_value": [1]})
        # X_5
        self.pc.add_gate({"name": "y", "target_qubit": [10],
                          "control_qubit": [19], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18, 4], "control_value": [1, 1]})
        self.pc.add_gate({"name": "x", "target_qubit": [18],
                          "control_qubit": [17], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18, 4], "control_value": [1, 0]})
        # X_6
        self.pc.add_gate({"name": "y", "target_qubit": [11],
                          "control_qubit": [19], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18], "control_value": [1]})
        # X_7
        self.pc.add_gate({"name": "y", "target_qubit": [12],
                          "control_qubit": [19], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18, 4], "control_value": [1, 1]})
        self.pc.add_gate({"name": "x", "target_qubit": [18],
                          "control_qubit": [17, 3], "control_value": [1, 1]})
        self.pc.add_gate({"name": "x", "target_qubit": [17],
                          "control_qubit": [16, 2], "control_value": [1, 1]})
        self.pc.add_gate({"name": "x", "target_qubit": [16],
                          "control_qubit": [0], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [18],
                          "control_qubit": [16, 3], "control_value": [1, 0]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18, 4], "control_value": [1, 0]})
        # X_8
        self.pc.add_gate({"name": "y", "target_qubit": [13],
                          "control_qubit": [19], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18], "control_value": [1]})
        # X_9
        self.pc.add_gate({"name": "y", "target_qubit": [14],
                          "control_qubit": [19], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [19],
                          "control_qubit": [18, 4], "control_value": [1, 1]})
        self.pc.add_gate({"name": "x", "target_qubit": [18],
                          "control_qubit": [16], "control_value": [1]})
        # X_10
        self.pc.add_gate({"name": "y", "target_qubit": [15],
                          "control_qubit": [18], "control_value": [1]})
        self.pc.add_gate({"name": "x", "target_qubit": [18],
                          "control_qubit": [16, 3], "control_value": [1, 1]})
        self.pc.add_gate({"name": "x", "target_qubit": [16],
                          "control_qubit": [0, 1], "control_value": [1, 1]})

        self.select_reg = [0, 1, 2, 3, 4]
        self.system_reg = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.ancilla_reg = [16, 17, 18, 19]

    def tearDown(self) -> None:
        del self.pc

    def test_regular(self,):
        val_in_select_reg_to_tgt_val = {
            "10000": {5: [0, 1],
                      6: [0, 0],
                      7: [0, 0],
                      8: [0, 0],
                      9: [0, 0],
                      10: [0, 0],
                      11: [0, 0],
                      12: [0, 0],
                      13: [0, 0],
                      14: [0, 0],
                      15: [0, 0]},
            "10001": {5: [0, 0],
                      6: [0, 1],
                      7: [0, 0],
                      8: [0, 0],
                      9: [0, 0],
                      10: [0, 0],
                      11: [0, 0],
                      12: [0, 0],
                      13: [0, 0],
                      14: [0, 0],
                      15: [0, 0]},
            "10010": {5: [0, 0],
                      6: [0, 0],
                      7: [0, 1],
                      8: [0, 0],
                      9: [0, 0],
                      10: [0, 0],
                      11: [0, 0],
                      12: [0, 0],
                      13: [0, 0],
                      14: [0, 0],
                      15: [0, 0]}
        }
        for val_in_select_reg, expect_tgt_val in \
                val_in_select_reg_to_tgt_val.items():

            actual_tgt_val = get_tgt_val(
                val_in_ctrl_reg=val_in_select_reg,
                pc=self.pc,
                tgt_reg=self.system_reg,
                ctrl_reg=self.select_reg,
                ancilla_reg=self.ancilla_reg
            )
            self.assertDictEqual(expect_tgt_val, actual_tgt_val)
