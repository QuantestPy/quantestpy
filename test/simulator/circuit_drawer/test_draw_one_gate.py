import unittest

from quantestpy import PauliCircuit
from quantestpy.simulator.circuit_drawer import CircuitDrawer as CD


class TestDrawOneGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.circuit_drawer.test_draw_one_gate
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK
    $
    """

    def test_regular(self,):
        pc = PauliCircuit(5)
        pc.add_gate({"name": "x", "control_qubit": [0, 2], "target_qubit": [3],
                     "control_value": [1, 0]})
        cd = CD(pc)

        cd.draw_one_gate(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "─\033[0m■\033[0m─\033[0m",
                  1: " │ \033[0m",
                  2: "─\033[0m┼\033[0m─\033[0m",
                  3: " │ \033[0m",
                  4: "─\033[0mo\033[0m─\033[0m",
                  5: " │ \033[0m",
                  6: "[X]\033[0m",
                  7: "   ",
                  8: "───\033[0m"}
        self.assertEqual(actual, expect)
