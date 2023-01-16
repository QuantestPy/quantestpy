import unittest

from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer as CD


class TestDrawRest(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.quantestpy_circuit_drawer.test_draw_rest
    .
    ----------------------------------------------------------------------
    Ran 1 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        qc = QuantestPyCircuit(5)
        cd = CD(qc)
        cd._occupied_line_id = [0, 1, 6]

        cd.draw_rest()
        actual = cd._line_id_to_text
        expect = {0: "",
                  1: "",
                  2: "─",
                  3: " ",
                  4: "─",
                  5: " ",
                  6: "",
                  7: " ",
                  8: "─"}
        self.assertEqual(actual, expect)

        actual = cd._occupied_line_id
        expect = [0, 1, 6, 2, 3, 4, 5, 7, 8]
        self.assertEqual(actual, expect)
