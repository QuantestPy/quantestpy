import unittest

from quantestpy import PauliCircuit
from quantestpy.simulator.circuit_drawer import CircuitDrawer as CD


class TestDrawInitVector(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.circuit_drawer.test_draw_init_vector
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK
    $
    """

    def test_default(self,):
        pc = PauliCircuit(4)
        pc.set_qubit_value(qubit_idx=[0, 1, 2, 3], qubit_val=[0, 1, 0, 1])
        cd = CD(pc)

        cd.draw_init_vector()
        actual = cd.line_id_to_text
        expect = {0: "|0>\033[0m",
                  1: "   ",
                  2: "|1>\033[0m",
                  3: "   ",
                  4: "|0>\033[0m",
                  5: "   ",
                  6: "|1>\033[0m"}
        self.assertEqual(actual, expect)
