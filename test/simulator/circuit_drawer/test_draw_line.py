import unittest

from quantestpy import PauliCircuit
from quantestpy.simulator.circuit_drawer import CircuitDrawer as CD


class TestDrawLine(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.circuit_drawer.test_draw_line
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        pc = PauliCircuit(3)
        cd = CD(pc)

        cd.draw_line()
        actual = cd.line_id_to_text
        expect = {0: "─\033[0m",
                  1: " ",
                  2: "─\033[0m",
                  3: " ",
                  4: "─\033[0m"}
        self.assertEqual(actual, expect)

    def test_with_color(self,):
        pc = PauliCircuit(3)
        pc.set_qubit_value(qubit_idx=[0, 1, 2], qubit_val=[1, 0, 1])
        cd = CD(pc)
        cd._color_code_line_0 = ""
        cd._color_code_line_1 = "\033[32m"

        cd.draw_line()
        actual = cd.line_id_to_text
        expect = {0: "\033[32m─\033[0m",
                  1: " ",
                  2: "─\033[0m",
                  3: " ",
                  4: "\033[32m─\033[0m"}
        self.assertEqual(actual, expect)
