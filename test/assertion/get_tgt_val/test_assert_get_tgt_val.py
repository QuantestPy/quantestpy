import unittest

from quantestpy import PauliCircuit, assert_get_tgt_val


class TestAssertGetTgtVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.assertion.get_tgt_val.test_assert_get_tgt_val
    .
    ----------------------------------------------------------------------
    Ran 1 tests in 0.044s

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
        qubit_idx_to_val_in_select_reg_to_tgt_val = \
            assert_get_tgt_val(
                circuit=self.pc,
                tgt_reg=self.system_reg,
                ctrl_reg=self.select_reg,
                ancilla_reg=self.ancilla_reg,
                print_out_result=False,
                check_ancilla_is_uncomputed=True
            )

        # check qubit idx 6
        expected_tgt_val_for_qubit_idx_6 = {
            "10000": [0, 0],
            "10001": [0, 1],
            "10010": [0, 0],
            "10011": [0, 0],
            "10100": [0, 0],
            "10101": [0, 0],
            "10110": [0, 0],
            "10111": [0, 0],
            "11000": [0, 0],
            "11001": [0, 0],
            "11010": [0, 0]
        }
        for val_in_select_reg, tgt_val in \
                expected_tgt_val_for_qubit_idx_6.items():
            self.assertEqual(
                tgt_val,
                qubit_idx_to_val_in_select_reg_to_tgt_val[6][
                    val_in_select_reg]
            )

        # check qubit idx
        self.assertEqual(
            1,
            qubit_idx_to_val_in_select_reg_to_tgt_val[14]["11001"][-1]
        )
