import unittest

from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer as CD


class TestDrawLine(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.quantestpy_circuit_drawer.test_draw_line
    .
    ----------------------------------------------------------------------
    Ran 1 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        qc = QuantestPyCircuit(3)
        cd = CD(qc)

        cd.draw_line()
        actual = cd._line_id_to_text
        expect = {0: "─",
                  1: " ",
                  2: "─",
                  3: " ",
                  4: "─"}
        self.assertEqual(actual, expect)
