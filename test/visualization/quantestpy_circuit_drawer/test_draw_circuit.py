import unittest

from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer as CD


class TestDrawCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.quantestpy_circuit_drawer.test_draw_circuit
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        qc = QuantestPyCircuit(5)
        qc.add_gate({"name": "x", "control_qubit": [0, 2], "target_qubit": [3],
                     "control_value": [1, 0]})
        cd = CD(qc)

        cd.draw_circuit()
        actual = cd.line_id_to_text_whole
        expect = \
            {0: "0 ──■── 0",
             1: "    │    ",
             2: "1 ──┼── 1",
             3: "    │    ",
             4: "2 ──o── 2",
             5: "    │    ",
             6: "3 ─[X]─ 3",
             7: "         ",
             8: "4 ───── 4"}
        self.assertEqual(actual, expect)
