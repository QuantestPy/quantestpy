import unittest

from quantestpy import PauliCircuit
from quantestpy.simulator.circuit_drawer import CircuitDrawer as CD


class TestDrawTgt(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.circuit_drawer.test_draw_tgt
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.003s

    OK
    $
    """

    def test_regular(self,):
        pc = PauliCircuit(2)
        pc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [1],
                     "control_value": []})
        cd = CD(pc)

        cd.draw_tgt(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "",
                  1: "",
                  2: "[X]\033[0m"}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [2]
        self.assertEqual(actual, expect)

    def test_multi(self,):
        pc = PauliCircuit(2)
        pc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [0, 1],
                     "control_value": []})
        cd = CD(pc)

        cd.draw_tgt(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "[X]\033[0m",
                  1: "",
                  2: "[X]\033[0m"}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [0, 2]
        self.assertEqual(actual, expect)

    def test_with_ctrl(self,):
        pc = PauliCircuit(3)
        pc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [1],
                     "control_value": []})
        pc.add_gate({"name": "y", "control_qubit": [0, 1], "target_qubit": [2],
                     "control_value": [1, 1]})
        cd = CD(pc)

        cd.draw_tgt(gate_id=1)
        actual = cd.line_id_to_text
        expect = {0: "",
                  1: "",
                  2: "",
                  3: "",
                  4: "[Y]\033[0m"}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [4]
        self.assertEqual(actual, expect)

    def test_with_color(self,):
        pc = PauliCircuit(3)
        pc.add_gate({"name": "z", "control_qubit": [0], "target_qubit": [1, 2],
                     "control_value": [1]})
        cd = CD(pc)
        cd._color_code_tgt = "\033[31m"

        cd.draw_tgt(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "",
                  1: "",
                  2: "\033[31m[Z]\033[0m",
                  3: "",
                  4: "\033[31m[Z]\033[0m"}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [2, 4]
        self.assertEqual(actual, expect)
