import unittest

from quantestpy import PauliCircuit
from quantestpy.simulator.circuit_drawer import CircuitDrawer as CD


class TestDrawCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.circuit_drawer.test_draw_circuit
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s

    OK
    $
    """

    def test_regular(self,):
        pc = PauliCircuit(5)
        pc.set_qubit_value(qubit_idx=[0], qubit_val=[1])
        pc.add_gate({"name": "x", "control_qubit": [0, 2], "target_qubit": [3],
                     "control_value": [1, 0]})
        cd = CD(pc)

        cd.draw_circuit()
        actual = cd.line_id_to_text
        expect = \
            {0:
             "0 \033[0m |1>\033[0m ─\033[0m─\033[0m■\033[0m─\033[0m─\033[0m",
             1: "         │ \033[0m ",
             2:
             "1 \033[0m |0>\033[0m ─\033[0m─\033[0m┼\033[0m─\033[0m─\033[0m",
             3: "         │ \033[0m ",
             4:
             "2 \033[0m |0>\033[0m ─\033[0m─\033[0mo\033[0m─\033[0m─\033[0m",
             5: "         │ \033[0m ",
             6: "3 \033[0m |0>\033[0m ─\033[0m[X]\033[0m─\033[0m",
             7: "            ",
             8: "4 \033[0m |0>\033[0m ─\033[0m───\033[0m─\033[0m"}
        self.assertEqual(actual, expect)

    def test_color(self,):
        pc = PauliCircuit(5)
        pc.set_qubit_value(qubit_idx=[0], qubit_val=[1])
        pc.add_gate({"name": "x", "control_qubit": [0, 2], "target_qubit": [3],
                     "control_value": [1, 0]})
        cd = CD(pc)
        cd._color_code_line_1 = "\033[32m"

        cd.draw_circuit()
        actual = cd.line_id_to_text
        expect = \
            {0: "0 \033[0m \033[32m|1>\033[0m \033[32m─\033[0m\033[32m─"
                + "\033[0m\033[32m■\033[0m\033[32m─\033[0m\033[32m─\033[0m",
             1: "         │ \033[0m ",
             2:
             "1 \033[0m |0>\033[0m ─\033[0m─\033[0m┼\033[0m─\033[0m─\033[0m",
             3: "         │ \033[0m ",
             4:
             "2 \033[0m |0>\033[0m ─\033[0m─\033[0mo\033[0m─\033[0m─\033[0m",
             5: "         │ \033[0m ",
             6: "3 \033[0m |0>\033[0m ─\033[0m[X]\033[0m\033[32m─\033[0m",
             7: "            ",
             8: "4 \033[0m |0>\033[0m ─\033[0m───\033[0m─\033[0m"}
        self.assertEqual(actual, expect)
