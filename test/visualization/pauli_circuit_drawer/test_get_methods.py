import unittest

import numpy as np

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.pauli_circuit_drawer import \
    PauliCircuitDrawer as CD


class TestGetMethods(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m \
        unittest test.visualization.pauli_circuit_drawer.test_get_methods
    ........
    ----------------------------------------------------------------------
    Ran 8 tests in 0.003s

    OK
    $
    """

    def test_get_color_code_line(self,):
        pc = PauliCircuit(10)
        cd = CD(pc)
        cd._color_code_line_0 = "\033[32m"
        cd._color_code_line_1 = "\033[35m"

        self.assertEqual(cd.get_color_code_line(qubit_val=0), "\033[32m")
        self.assertEqual(cd.get_color_code_line(qubit_val=1), "\033[35m")

    def test_get_line(self,):
        actual = CD.get_line(1, length=4, color_code="\033[32m")
        expect = "\033[32m────\033[0m"
        self.assertEqual(actual, expect)

    def test_get_cross_line(self,):
        actual = CD.get_cross_line(
            1, color_code_cross="\033[31m", color_code_line="\033[32m")
        expect = "\033[32m─\033[0m\033[31m┼\033[0m\033[32m─\033[0m"
        self.assertEqual(actual, expect)

    def test_get_wire(self,):
        actual = CD.get_wire(color_code="\033[32m")
        expect = "\033[32m │ \033[0m"
        self.assertEqual(actual, expect)

    def test_get_tgt(self,):
        name_lst = ["x", "y", "z", "swap"]
        obj_lst = ["[X]", "[Y]", "[Z]", "SWP"]
        for name, obj in zip(name_lst, obj_lst):
            actual = CD.get_tgt(name, 1, color_code="\033[35m")
            expect = "\033[35m" + obj + "\033[0m"
            self.assertEqual(actual, expect)

    def test_get_ctrl(self,):
        ctrl_val_lst = [1, 0]
        obj_lst = ["■", "o"]
        for ctrl_val, obj in zip(ctrl_val_lst, obj_lst):
            actual = CD.get_ctrl(ctrl_val, 1, color_code_ctrl="\033[31m",
                                 color_code_line="\033[32m")
            expect = "\033[32m─\033[0m\033[31m" + \
                obj + "\033[0m\033[32m─\033[0m"
            self.assertEqual(actual, expect)

    def test_get_state(self,):
        qubit_val_lst = [1, 0]
        obj_lst = ["|1>", "|0>"]
        color_code_lst = ["\033[32m", ""]
        for qubit_val, obj, cc in zip(qubit_val_lst, obj_lst, color_code_lst):
            actual = CD.get_state(qubit_val, color_code=cc)
            expect = cc + obj + "\033[0m"
            self.assertEqual(actual, expect)

    def test_get_phase(self,):
        qubit_phase = 1.5 * np.pi
        actual = CD.get_phase(qubit_phase=qubit_phase, decimals=2)
        expect = "1.5\033[0m"
        self.assertEqual(actual, expect)
