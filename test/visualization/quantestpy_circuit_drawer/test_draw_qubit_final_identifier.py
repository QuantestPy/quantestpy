import unittest

from quantestpy.simulator.quantestpy_circuit import QuantestPyCircuit
from quantestpy.visualization.quantestpy_circuit_drawer import \
    QuantestPyCircuitDrawer as CD


class TestDrawQubitFinalIdentifier(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.quantestpy_circuit_drawer.test_draw_qubit_final_identifier
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_small_qubit(self,):
        qc = QuantestPyCircuit(3)
        cd = CD(qc)

        cd.draw_qubit_final_identifier()
        actual = cd._line_id_to_text
        expect = {0: "0",
                  1: " ",
                  2: "1",
                  3: " ",
                  4: "2"}
        self.assertEqual(actual, expect)

    def test_large_qubit(self,):
        qc = QuantestPyCircuit(11)
        cd = CD(qc)

        cd.draw_qubit_final_identifier()
        actual = cd._line_id_to_text
        expect = {0: "0 ",
                  1: "  ",
                  2: "1 ",
                  3: "  ",
                  4: "2 ",
                  5: "  ",
                  6: "3 ",
                  7: "  ",
                  8: "4 ",
                  9: "  ",
                  10: "5 ",
                  11: "  ",
                  12: "6 ",
                  13: "  ",
                  14: "7 ",
                  15: "  ",
                  16: "8 ",
                  17: "  ",
                  18: "9 ",
                  19: "  ",
                  20: "10"}
        self.assertEqual(actual, expect)
