import unittest

from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer as CD


class TestDrawOneGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.quantestpy_circuit_drawer.test_draw_one_gate
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK
    $
    """

    def test_regular(self,):
        qc = QuantestPyCircuit(5)
        qc.add_gate({"name": "x", "control_qubit": [0, 2], "target_qubit": [3],
                     "control_value": [1, 0]})
        cd = CD(qc)

        cd.draw_one_gate(gate_id=0)
        actual = cd._line_id_to_text
        expect = {0: "─■─",
                  1: " │ ",
                  2: "─┼─",
                  3: " │ ",
                  4: "─o─",
                  5: " │ ",
                  6: "[X]",
                  7: "   ",
                  8: "───"}
        self.assertEqual(actual, expect)
