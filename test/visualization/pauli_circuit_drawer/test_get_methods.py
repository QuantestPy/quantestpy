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

    def test_get_tgt(self,):
        name_lst = ["x", "y", "z", "swap"]
        obj_lst = ["[X]", "[Y]", "[Z]", "[SWP]"]
        for name, obj in zip(name_lst, obj_lst):
            actual = CD.get_tgt(name)
            expect = obj
            self.assertEqual(actual, expect)

    def test_get_state(self,):
        qubit_val_lst = [1, 0]
        obj_lst = ["|1>", "|0>"]
        for qubit_val, obj in zip(qubit_val_lst, obj_lst):
            actual = CD.get_state(qubit_val)
            expect = obj
            self.assertEqual(actual, expect)

    def test_get_phase(self,):
        pc = PauliCircuit(10)
        cd = CD(pc)
        qubit_phase = 1.5 * np.pi
        actual = cd.get_phase(qubit_phase=qubit_phase)
        expect = "1.5"
        self.assertEqual(actual, expect)
