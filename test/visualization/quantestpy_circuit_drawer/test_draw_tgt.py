import unittest

from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer as CD


class TestDrawTgt(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.quantestpy_circuit_drawer.test_draw_tgt
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.002s

    OK
    $
    """

    def test_single(self,):
        qc = QuantestPyCircuit(2)
        qc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [1],
                     "control_value": []})
        cd = CD(qc)

        cd.draw_tgt(gate_id=0)
        actual = cd._line_id_to_text
        expect = {0: "",
                  1: "",
                  2: "[X]"}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [2]
        self.assertEqual(actual, expect)

    def test_multi(self,):
        qc = QuantestPyCircuit(2)
        qc.add_gate({"name": "h", "control_qubit": [], "target_qubit": [0, 1],
                     "control_value": []})
        cd = CD(qc)

        cd.draw_tgt(gate_id=0)
        actual = cd._line_id_to_text
        expect = {0: "[H]",
                  1: "",
                  2: "[H]"}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [0, 2]
        self.assertEqual(actual, expect)

    def test_with_ctrl(self,):
        qc = QuantestPyCircuit(3)
        qc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [1],
                     "control_value": []})
        qc.add_gate({"name": "rz", "control_qubit": [0, 1],
                     "target_qubit": [2], "control_value": [1, 1]})
        cd = CD(qc)

        cd.draw_tgt(gate_id=1)
        actual = cd._line_id_to_text
        expect = {0: "",
                  1: "",
                  2: "",
                  3: "",
                  4: "[R_z]"}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [4]
        self.assertEqual(actual, expect)
