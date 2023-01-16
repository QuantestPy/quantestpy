import unittest

from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer as CD


class TestDrawCtrl(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.quantestpy_circuit_drawer.test_draw_ctrl
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.002s

    OK
    $
    """

    def test_single(self,):
        qc = QuantestPyCircuit(2)
        qc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
                     "control_value": [1]})
        cd = CD(qc)

        cd.draw_ctrl(gate_id=0)
        actual = cd._line_id_to_text
        expect = {0: "■",
                  1: "",
                  2: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [0]
        self.assertEqual(actual, expect)

    def test_multi(self,):
        qc = QuantestPyCircuit(3)
        qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                     "control_value": [1, 0]})
        cd = CD(qc)

        cd.draw_ctrl(gate_id=0)
        actual = cd._line_id_to_text
        expect = {0: "■",
                  1: "",
                  2: "o",
                  3: "",
                  4: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [0, 2]
        self.assertEqual(actual, expect)
