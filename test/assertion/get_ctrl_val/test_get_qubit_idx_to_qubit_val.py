import unittest

from quantestpy import PauliCircuit
from quantestpy.assertion.get_ctrl_val import \
    _get_qubit_idx_to_qubit_val_for_given_val_in_ctrl_reg as get_ctrl_val


class TestGetQubitIdxToQubitVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.get_ctrl_val.test_get_qubit_idx_to_qubit_val
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
        val_in_select_reg_to_ctrl_val = {
            "10000": {0: [1, 1, 1],
                      1: [0, 0],
                      2: [0, 0],
                      3: [0, 0, 0, 0, 0, 0],
                      4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      16: [1, 1, 1, 0, 0, 0],
                      17: [1, 1, 1, 0, 0, 0],
                      18: [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      19: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
            "11001": {0: [1, 1, 1],
                      1: [1, 1],
                      2: [0, 0],
                      3: [0, 0, 0, 0, 0, 0],
                      4: [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                      16: [0, 0, 0, 1, 1, 1],
                      17: [0, 0, 0, 0, 0, 0],
                      18: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                      19: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]},
            "11010": {0: [1, 1, 1],
                      1: [1, 1],
                      2: [0, 0],
                      3: [1, 1, 1, 1, 1, 1],
                      4: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      16: [0, 0, 0, 1, 1, 1],
                      17: [0, 0, 0, 0, 0, 0],
                      18: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                      19: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
        }
        for val_in_select_reg, expect_ctrl_val in \
                val_in_select_reg_to_ctrl_val.items():

            actual_ctrl_val = get_ctrl_val(
                val_in_ctrl_reg=val_in_select_reg,
                pc=self.pc,
                ctrl_reg=self.select_reg,
                ancilla_reg=self.ancilla_reg
            )
            self.assertDictEqual(expect_ctrl_val, actual_ctrl_val)
