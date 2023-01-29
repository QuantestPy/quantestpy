import unittest

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.pauli_circuit_drawer import \
    PauliCircuitDrawer as CD


class TestDrawCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.pauli_circuit_drawer.test_draw_circuit
    .
    ----------------------------------------------------------------------
    Ran 1 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        pc = PauliCircuit(5)
        pc.set_qubit_value(qubit_idx=[0], qubit_val=[1])
        pc.add_gate({"name": "x", "control_qubit": [0, 2], "target_qubit": [3],
                     "control_value": [1, 0]})
        cd = CD(pc)
        cd._color_code_line_1 = ""

        cd.draw_circuit()
        actual = cd.line_id_to_text_whole
        expect = \
            {0: "0 |1> 0.0 ─\033[0m─\033[0m\033[34m■"
                + "\033[0m─\033[0m─\033[0m |1> 0.0 0",
             1: "            \033[34m│\033[0m            ",
             2: "1 |0> 0.0 ─\033[0m─\033[0m\033[34m┼"
                + "\033[0m─\033[0m─\033[0m |0> 0.0 1",
             3: "            \033[34m│\033[0m            ",
             4: "2 |0> 0.0 ─\033[0m─\033[0m\033[34mo"
                + "\033[0m─\033[0m─\033[0m |0> 0.0 2",
             5: "            \033[34m│\033[0m            ",
             6: "3 |0> 0.0 ─\033[0m\033[34m[X]\033[0m─\033[0m |1> 0.0 3",
             7: "                         ",
             8: "4 |0> 0.0 ─\033[0m─\033[0m──\033[0m─\033[0m |0> 0.0 4"}
        self.assertEqual(actual, expect)
