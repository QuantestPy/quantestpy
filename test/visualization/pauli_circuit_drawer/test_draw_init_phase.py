import unittest

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.pauli_circuit_drawer import \
    PauliCircuitDrawer as CD


class TestDrawInitPhase(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.pauli_circuit_drawer.test_draw_init_phase
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK
    $
    """

    def test_default(self,):
        pc = PauliCircuit(4)
        cd = CD(pc)

        cd.draw_init_phase()
        actual = cd._line_id_to_text
        expect = {0: "0.0",
                  1: "   ",
                  2: "0.0",
                  3: "   ",
                  4: "0.0",
                  5: "   ",
                  6: "0.0"}
        self.assertEqual(actual, expect)
