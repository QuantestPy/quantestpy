import unittest

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.pauli_circuit_drawer import \
    PauliCircuitDrawer as CD


class TestDrawWire(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.visualization.pauli_circuit_drawer.test_draw_wire
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.002s

    OK
    $
    """

    def test_one_wire(self,):
        pc = PauliCircuit(3)
        pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                     "control_value": [1]})
        cd = CD(pc)

        cd.draw_wire(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "",
                  1: " │ \033[0m",
                  2: "",
                  3: "",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [1]
        self.assertEqual(actual, expect)

    def test_multi_wire(self,):
        pc = PauliCircuit(3)
        pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [2],
                     "control_value": [1]})
        cd = CD(pc)

        cd.draw_wire(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "",
                  1: " │ \033[0m",
                  2: "─\033[0m┼\033[0m─\033[0m",
                  3: " │ \033[0m",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [1, 2, 3]
        self.assertEqual(actual, expect)

    def test_color_line(self,):
        pc = PauliCircuit(3)
        pc.set_qubit_value(qubit_idx=[1], qubit_val=[1])
        pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [2],
                     "control_value": [1]})
        cd = CD(pc)
        cd._color_code_line_1 = "\033[32m"

        cd.draw_wire(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "",
                  1: " │ \033[0m",
                  2: "\033[32m─\033[0m┼\033[0m\033[32m─\033[0m",
                  3: " │ \033[0m",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [1, 2, 3]
        self.assertEqual(actual, expect)

    def test_color_wire(self,):
        pc = PauliCircuit(3)
        pc.set_qubit_value(qubit_idx=[1], qubit_val=[1])
        pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [2],
                     "control_value": [1]})
        cd = CD(pc)
        cd._color_code_line_1 = "\033[32m"
        cd._color_code_cross = "\033[31m"
        cd._color_code_wire = "\033[31m"

        cd.draw_wire(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "",
                  1: " │ \033[0m",
                  2: "\033[32m─\033[0m┼\033[0m\033[32m─\033[0m",
                  3: " │ \033[0m",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [1, 2, 3]
        self.assertEqual(actual, expect)
