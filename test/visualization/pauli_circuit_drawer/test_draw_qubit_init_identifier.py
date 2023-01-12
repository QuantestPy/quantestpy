import unittest

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.pauli_circuit_drawer import \
    PauliCircuitDrawer as CD


class TestDrawQubitInitIdentifier(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.pauli_circuit_drawer.test_draw_qubit_init_identifier
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.002s

    OK
    $
    """

    def test_default(self,):
        pc = PauliCircuit(3)
        cd = CD(pc)

        cd.draw_qubit_init_identifier()
        actual = cd.line_id_to_text
        expect = {0: "0\033[0m",
                  1: " ",
                  2: "1\033[0m",
                  3: " ",
                  4: "2\033[0m"}
        self.assertEqual(actual, expect)

    def test_reg_name(self,):
        pc = PauliCircuit(3)
        cd = CD(pc)
        cd._qubit_id_to_reg_name = {
            0: "reg_1",
            1: "",
            2: "reg_2"
        }

        cd.draw_qubit_init_identifier()
        actual = cd.line_id_to_text
        expect = {0: "0 reg_1\033[0m",
                  1: "       ",
                  2: "1 \033[0m     ",
                  3: "       ",
                  4: "2 reg_2\033[0m"}
        self.assertEqual(actual, expect)

    def test_color_code(self,):
        pc = PauliCircuit(3)
        cd = CD(pc)
        cd._qubit_id_to_color_code = {
            0: "",
            1: "\033[34m",
            2: "\033[35m"
        }

        cd.draw_qubit_init_identifier()
        actual = cd.line_id_to_text
        expect = {0: "0\033[0m",
                  1: " ",
                  2: "\033[34m1\033[0m",
                  3: " ",
                  4: "\033[35m2\033[0m"}
        self.assertEqual(actual, expect)

    def test_reg_name_color_code(self,):
        pc = PauliCircuit(3)
        cd = CD(pc)
        cd._qubit_id_to_reg_name = {
            0: "reg_1",
            1: "",
            2: " reg_2"
        }
        cd._qubit_id_to_color_code = {
            0: "",
            1: "\033[34m",
            2: "\033[35m"
        }

        cd.draw_qubit_init_identifier()
        actual = cd.line_id_to_text
        expect = {0: "0 reg_1\033[0m ",
                  1: "        ",
                  2: "\033[34m1 \033[0m      ",
                  3: "        ",
                  4: "\033[35m2  reg_2\033[0m"}
        self.assertEqual(actual, expect)
