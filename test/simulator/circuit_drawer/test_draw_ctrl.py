import unittest

from quantestpy import PauliCircuit
from quantestpy.simulator.circuit_drawer import CircuitDrawer as CD


class TestDrawCtrl(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.circuit_drawer.test_draw_ctrl
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.002s

    OK
    $
    """

    def test_single(self,):
        pc = PauliCircuit(2)
        pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                     "control_value": [1]})
        cd = CD(pc)

        cd.draw_ctrl(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "─\033[0m■\033[0m─\033[0m",
                  1: "",
                  2: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [0]
        self.assertEqual(actual, expect)

    def test_multi(self,):
        pc = PauliCircuit(3)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                     "control_value": [1, 0]})
        cd = CD(pc)

        cd.draw_ctrl(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "─\033[0m■\033[0m─\033[0m",
                  1: "",
                  2: "─\033[0mo\033[0m─\033[0m",
                  3: "",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [0, 2]
        self.assertEqual(actual, expect)

    def test_color_line(self,):
        pc = PauliCircuit(3)
        pc.set_qubit_value(qubit_idx=[0], qubit_val=[1])
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                     "control_value": [1, 0]})
        cd = CD(pc)
        cd._color_code_line_1 = "\033[32m"

        cd.draw_ctrl(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "\033[32m─\033[0m\033[32m■\033[0m\033[32m─\033[0m",
                  1: "",
                  2: "─\033[0mo\033[0m─\033[0m",
                  3: "",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [0, 2]
        self.assertEqual(actual, expect)

    def test_color_ctrl(self,):
        pc = PauliCircuit(3)
        pc.set_qubit_value(qubit_idx=[0], qubit_val=[1])
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                     "control_value": [1, 0]})
        cd = CD(pc)
        cd._color_code_line_1 = "\033[32m"
        cd._color_code_ctrl = "\033[31m"

        cd.draw_ctrl(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "\033[32m─\033[0m\033[31m■\033[0m\033[32m─\033[0m",
                  1: "",
                  2: "─\033[0m\033[31mo\033[0m─\033[0m",
                  3: "",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [0, 2]
        self.assertEqual(actual, expect)
