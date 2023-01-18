import unittest

from quantestpy.simulator.pauli_circuit import PauliCircuit
from quantestpy.visualization.pauli_circuit_drawer import \
    PauliCircuitDrawer as CD


class TestColorLine(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.visualization.pauli_circuit_drawer.test_color_line
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.001s

    OK
    $
    """

    def test_regular(self,):
        pc = PauliCircuit(2)
        pc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [0],
                     "control_value": []})
        pc._execute_all_gates()
        cd = CD(pc)

        cd._line_id_to_text = {
            0: "AAA",
            1: "",
            2: "CC"
        }
        cd.color_line()

        actual = cd._line_id_to_text
        expect = {
            0: "\033[32mAAA\033[0m",
            1: "",
            2: "CC\033[0m"
        }
        self.assertEqual(actual, expect)
