import unittest

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.pauli_circuit_drawer import \
    PauliCircuitDrawer as CD


class TestDrawRest(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.visualization.pauli_circuit_drawer.test_draw_rest
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        pc = PauliCircuit(5)
        cd = CD(pc)
        cd._occupied_line_id = [0, 1, 6]

        cd.draw_rest(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "",
                  1: "",
                  2: "───\033[0m",
                  3: "   ",
                  4: "───\033[0m",
                  5: "   ",
                  6: "",
                  7: "   ",
                  8: "───\033[0m"}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [0, 1, 6, 2, 3, 4, 5, 7, 8]
        self.assertEqual(actual, expect)

    def test_color(self,):
        pc = PauliCircuit(2)
        cd = CD(pc)
        cd._color_code_line_0 = "\033[34m"
        cd._occupied_line_id = [2]

        cd.draw_rest(gate_id=0)
        actual = cd.line_id_to_text
        expect = {0: "\033[34m───\033[0m",
                  1: "   ",
                  2: ""}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [2, 0, 1]
        self.assertEqual(actual, expect)
