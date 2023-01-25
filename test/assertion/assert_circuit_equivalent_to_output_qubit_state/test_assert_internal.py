import unittest

from quantestpy.assertion.assert_circuit_equivalent_to_output_qubit_state \
    import _assert_internal
from quantestpy.simulator.pauli_circuit import PauliCircuit


class TestAssertInternal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_circuit_equivalent_to_output_qubit_state.test_assert_internal
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.002s
    OK
    $
    """

    def test_return_none(self,):
        pc = PauliCircuit(5)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        pc.add_gate({"name": "y", "control_qubit": [0, 2], "target_qubit": [3],
                    "control_value": [1, 1]})

        self.assertIsNone(
            _assert_internal(
                pauli_circuit_org=pc,
                input_reg=[0, 1],
                output_reg=[2, 3],
                in_bitstring="01",
                out_bitstring="00",
                out_phase=[]
            )
        )

    def test_return_obj(self,):
        pc = PauliCircuit(4)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        pc.add_gate({"name": "y", "control_qubit": [0, 2], "target_qubit": [3],
                    "control_value": [1, 1]})

        out_bitstring_actual, out_phase_actual = \
            _assert_internal(pauli_circuit_org=pc,
                             input_reg=[0, 1],
                             output_reg=[0, 1, 2, 3],
                             in_bitstring="11",
                             out_bitstring="0000",
                             out_phase=[]
                             )
        self.assertEqual(out_bitstring_actual, "1111")
        self.assertEqual(out_phase_actual, [0, 0, 0, 0.5])
