import unittest

from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer as CD


class TestDrawWire(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.quantestpy_circuit_drawer.test_draw_wire
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.001s

    OK
    $
    """

    def test_one_wire(self,):
        qc = QuantestPyCircuit(3)
        qc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                     "control_value": [1]})
        cd = CD(qc)

        cd.draw_wire(gate_id=0)
        actual = cd._line_id_to_text
        expect = {0: "",
                  1: "│",
                  2: "",
                  3: "",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [1]
        self.assertEqual(actual, expect)

    def test_multi_wire(self,):
        qc = QuantestPyCircuit(3)
        qc.add_gate({"name": "h", "control_qubit": [0], "target_qubit": [2],
                     "control_value": [1]})
        cd = CD(qc)

        cd.draw_wire(gate_id=0)
        actual = cd._line_id_to_text
        expect = {0: "",
                  1: "│",
                  2: "┼",
                  3: "│",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [1, 2, 3]
        self.assertEqual(actual, expect)

    def test_multi_target(self,):
        qc = QuantestPyCircuit(3)
        qc.add_gate({"name": "x", "control_qubit": [],
                     "target_qubit": [0, 1, 2], "control_value": []})
        cd = CD(qc)

        cd.draw_wire(gate_id=0)
        actual = cd._line_id_to_text
        expect = {0: "",
                  1: "",
                  2: "",
                  3: "",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = []
        self.assertEqual(actual, expect)

    def test_multi_target_one_ctrl(self,):
        qc = QuantestPyCircuit(3)
        qc.add_gate({"name": "x", "control_qubit": [1],
                     "target_qubit": [0, 2], "control_value": [1]})
        cd = CD(qc)

        cd.draw_wire(gate_id=0)
        actual = cd._line_id_to_text
        expect = {0: "",
                  1: "│",
                  2: "",
                  3: "│",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [1, 3]
        self.assertEqual(actual, expect)
