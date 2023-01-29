import unittest

from quantestpy.assertion.assert_circuit_equivalent_to_output_qubit_state \
    import PauliCircuitDrawerColorErrorQubit as CD
from quantestpy.simulator.pauli_circuit import PauliCircuit


class TestDrawer(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_circuit_equivalent_to_output_qubit_state.test_drawer
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.002s

    OK
    $
    """

    def test_draw_final_vector_regular(self,):
        pc = PauliCircuit(4)
        pc.set_qubit_value(qubit_idx=[0, 1, 2, 3], qubit_val=[0, 1, 0, 1])
        cd = CD(circuit=pc,
                output_reg=[0, 1, 3],
                val_err_reg=[1],
                color_phase=False,
                phase_err_reg=[])

        cd.draw_final_vector()
        actual = cd._line_id_to_text
        expect = {0: "\033[36m|0>\033[0m",
                  1: "   ",
                  2: "\033[31m|1>\033[0m",
                  3: "   ",
                  4: "|0>\033[0m",
                  5: "   ",
                  6: "\033[36m|1>\033[0m"}
        self.assertEqual(actual, expect)

    def test_draw_final_phase_regular(self,):
        pc = PauliCircuit(4)
        pc.add_gate({"name": "y", "control_qubit": [], "target_qubit": [1],
                     "control_value": []})
        pc.add_gate({"name": "z", "control_qubit": [], "target_qubit": [2],
                     "control_value": []})
        pc._execute_all_gates()
        cd = CD(circuit=pc,
                output_reg=[0, 3],
                val_err_reg=[],
                color_phase=True,
                phase_err_reg=[0])

        cd.draw_final_phase()
        actual = cd._line_id_to_text
        expect = {0: "\033[31m0.0\033[0m",
                  1: "   ",
                  2: "0.5\033[0m",
                  3: "   ",
                  4: "0.0\033[0m",
                  5: "   ",
                  6: "\033[36m0.0\033[0m"}
        self.assertEqual(actual, expect)
