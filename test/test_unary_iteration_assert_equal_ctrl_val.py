import unittest

from quantestpy import FastTestCircuit
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError
from quantestpy.unary_iteration import \
    assert_equal_ctrl_val_of_all_ops_on_syst_reg


class TestUnaryIterAssertEqualCtrlVal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_unary_iteration_assert_equal_ctrl_val
    .......
    ----------------------------------------------------------------------
    Ran 7 tests in 0.041s

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
        self.accumulate_reg = []

        self.val_in_select_to_ctrl = {
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

    def tearDown(self) -> None:
        del self.ftc

    def test_regular(self,):
        val_in_select_to_ctrl = self.val_in_select_to_ctrl
        self.assertIsNone(
            assert_equal_ctrl_val_of_all_ops_on_syst_reg(
                circuit=self.ftc,
                select_reg=self.select_reg,
                system_reg=self.system_reg,
                accumulate_reg=self.accumulate_reg,
                ctrl_reg=self.ctrl_reg,
                ctrl_val=self.ctrl_val,
                ancilla_reg=self.ancilla_reg,
                expected_val_in_select_reg_to_ctrl_val=val_in_select_to_ctrl
            )
        )

    def test_raise_from_inappropriate_input_type(self,):
        val_in_select_to_ctrl = \
            [[1], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]
        expected_err_msg = \
            "expected_val_in_select_reg_to_ctrl_val must be dict type."

        with self.assertRaises(QuantestPyError) as cm:
            assert_equal_ctrl_val_of_all_ops_on_syst_reg(
                circuit=self.ftc,
                select_reg=self.select_reg,
                system_reg=self.system_reg,
                accumulate_reg=self.accumulate_reg,
                ctrl_reg=self.ctrl_reg,
                ctrl_val=self.ctrl_val,
                ancilla_reg=self.ancilla_reg,
                expected_val_in_select_reg_to_ctrl_val=val_in_select_to_ctrl
            )
        self.assertEqual(cm.exception.args[0], expected_err_msg)

    def test_raise_from_inappropriate_key_type(self,):
        val_in_select_to_ctrl = \
            {1111: [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1]]}
        expected_err_msg = \
            "val_in_select_reg as keys in " \
            + "expected_val_in_select_reg_to_ctrl_val must be string type."

        with self.assertRaises(QuantestPyError) as cm:
            assert_equal_ctrl_val_of_all_ops_on_syst_reg(
                circuit=self.ftc,
                select_reg=self.select_reg,
                system_reg=self.system_reg,
                accumulate_reg=self.accumulate_reg,
                ctrl_reg=self.ctrl_reg,
                ctrl_val=self.ctrl_val,
                ancilla_reg=self.ancilla_reg,
                expected_val_in_select_reg_to_ctrl_val=val_in_select_to_ctrl
            )
        self.assertEqual(cm.exception.args[0], expected_err_msg)

    def test_raise_from_inappropriate_key_length(self,):
        val_in_select_to_ctrl = \
            {"00001": [[0], [1], [0], [0], [0], [0], [0], [0], [0], [0], [0]]}
        expected_err_msg = "Length of val_in_select_reg as keys in " \
            + "expected_val_in_select_reg_to_ctrl_val is not " \
            + "consistent with length of select_reg."

        with self.assertRaises(QuantestPyError) as cm:
            assert_equal_ctrl_val_of_all_ops_on_syst_reg(
                circuit=self.ftc,
                select_reg=self.select_reg,
                system_reg=self.system_reg,
                accumulate_reg=self.accumulate_reg,
                ctrl_reg=self.ctrl_reg,
                ctrl_val=self.ctrl_val,
                ancilla_reg=self.ancilla_reg,
                expected_val_in_select_reg_to_ctrl_val=val_in_select_to_ctrl
            )
        self.assertEqual(cm.exception.args[0], expected_err_msg)

    def test_raise_from_non_consistent_ops_number(self,):
        val_in_select_to_ctrl = \
            {"0000": [[1], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]],
             "0011": [[0], [0], [0], [1], [0], [0], [0], [0], [0], [0]]}
        expected_err_msg = "The numbers of ops are not consistent " \
            + "when val in select reg is 0011:\n" \
            + "expect: 10\n" \
            + "actual: 11"

        with self.assertRaises(QuantestPyAssertionError) as cm:
            assert_equal_ctrl_val_of_all_ops_on_syst_reg(
                circuit=self.ftc,
                select_reg=self.select_reg,
                system_reg=self.system_reg,
                accumulate_reg=self.accumulate_reg,
                ctrl_reg=self.ctrl_reg,
                ctrl_val=self.ctrl_val,
                ancilla_reg=self.ancilla_reg,
                expected_val_in_select_reg_to_ctrl_val=val_in_select_to_ctrl
            )
        self.assertEqual(cm.exception.args[0], expected_err_msg)

    def test_raise_from_assertion_non_equal(self,):
        val_in_select_to_ctrl = \
            {"0000": [[0], [1], [0], [0], [0], [0], [0], [0], [0], [0], [0]]}
        expected_err_msg = "Ctrl val(s) do not agree with your expectation " \
            + "when val in select reg is 0000:\n" \
            + "expect: " \
            + "[[0], [1], [0], [0], [0], [0], [0], [0], [0], [0], [0]].\n" \
            + "actual: " \
            + "[[1], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]]."

        with self.assertRaises(QuantestPyAssertionError) as cm:
            assert_equal_ctrl_val_of_all_ops_on_syst_reg(
                circuit=self.ftc,
                select_reg=self.select_reg,
                system_reg=self.system_reg,
                accumulate_reg=self.accumulate_reg,
                ctrl_reg=self.ctrl_reg,
                ctrl_val=self.ctrl_val,
                ancilla_reg=self.ancilla_reg,
                expected_val_in_select_reg_to_ctrl_val=val_in_select_to_ctrl
            )
        self.assertEqual(cm.exception.args[0], expected_err_msg)

    def test_raise_from_ancilla_not_uncomputated(self,):
        val_in_select_to_ctrl = \
            {"1111": [[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [1]]}
        self.ftc._gates[-1] = \
            {"name": "x", "target_qubit": [16],
             "control_qubit": [0, 1], "control_value": [0, 0]}
        expected_err_msg = "ancilla reg is not uncomputated to 0 " \
            + "when val in select reg is 1111."

        with self.assertRaises(QuantestPyAssertionError) as cm:
            assert_equal_ctrl_val_of_all_ops_on_syst_reg(
                circuit=self.ftc,
                select_reg=self.select_reg,
                system_reg=self.system_reg,
                accumulate_reg=self.accumulate_reg,
                ctrl_reg=self.ctrl_reg,
                ctrl_val=self.ctrl_val,
                ancilla_reg=self.ancilla_reg,
                expected_val_in_select_reg_to_ctrl_val=val_in_select_to_ctrl
            )
        self.assertEqual(cm.exception.args[0], expected_err_msg)
