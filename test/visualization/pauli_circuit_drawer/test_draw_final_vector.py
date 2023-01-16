import unittest

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.pauli_circuit_drawer import \
    PauliCircuitDrawer as CD


class TestDrawFinalVector(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.pauli_circuit_drawer.test_draw_final_vector
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
        cd._color_code_line_1 = ""

        cd.draw_final_vector()
        actual = cd._line_id_to_text
        expect = {0: "|0>",
                  1: "   ",
                  2: "|1>",
                  3: "   ",
                  4: "|0>",
                  5: "   ",
                  6: "|1>"}
        self.assertEqual(actual, expect)
