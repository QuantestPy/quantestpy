import unittest

from quantestpy import PauliCircuit
from quantestpy.simulator.circuit_drawer import CircuitDrawer as CD


class TestDrawSpace(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.circuit_drawer.test_draw_space
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK
    $
    """

    def test_default(self,):
        pc = PauliCircuit(3)
        cd = CD(pc)

        cd.draw_space()
        actual = cd.line_id_to_text
        expect = {0: " ",
                  1: " ",
                  2: " ",
                  3: " ",
                  4: " "}
        self.assertEqual(actual, expect)
