import unittest

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.pauli_circuit_drawer import \
    PauliCircuitDrawer as CD


class TestDrawFinalPhase(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.pauli_circuit_drawer.test_draw_final_phase
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK
    $
    """

    def test_default(self,):
        pc = PauliCircuit(4)
        pc.add_gate({"name": "y", "control_qubit": [], "target_qubit": [1],
                     "control_value": []})
        pc.add_gate({"name": "z", "control_qubit": [], "target_qubit": [2],
                     "control_value": []})
        pc._execute_all_gates()
        cd = CD(pc)

        cd.draw_final_phase()
        actual = cd.line_id_to_text
        expect = {0: "0.0\033[0m",
                  1: "   ",
                  2: "0.5\033[0m",
                  3: "   ",
                  4: "0.0\033[0m",
                  5: "   ",
                  6: "0.0\033[0m"}
        self.assertEqual(actual, expect)
