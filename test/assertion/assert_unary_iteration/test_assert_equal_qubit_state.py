import unittest

from quantestpy.assertion.assert_unary_iteration import \
    _assert_equal_qubit_state_replacing_gates_in_sys_reg_with_x_gates
from quantestpy.simulator.pauli_circuit import PauliCircuit


class TestAssertEqualQubitState(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_unary_iteration.test_assert_equal_qubit_state
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s
    OK
    $
    """

    def test_return_none(self):
        pc = PauliCircuit(5)
        pc.add_gate({"name": "z", "control_qubit": [0], "target_qubit": [2],
                    "control_value": [1]})
        pc.add_gate({"name": "y", "control_qubit": [0, 1], "target_qubit": [3],
                    "control_value": [1, 1]})

        self.assertIsNone(
            _assert_equal_qubit_state_replacing_gates_in_sys_reg_with_x_gates(
                pauli_circuit_org=pc,
                index_reg=[0, 1],
                system_reg=[2, 3, 4],
                in_bitstring="10",
                out_bitstring="100"
            )
        )

    def test_return_str(self):
        pc = PauliCircuit(5)
        pc.add_gate({"name": "z", "control_qubit": [0], "target_qubit": [2],
                    "control_value": [1]})
        pc.add_gate({"name": "y", "control_qubit": [0, 1], "target_qubit": [3],
                    "control_value": [1, 1]})

        output = \
            _assert_equal_qubit_state_replacing_gates_in_sys_reg_with_x_gates(
                pauli_circuit_org=pc,
                index_reg=[0, 1],
                system_reg=[2, 3, 4],
                in_bitstring="11",
                out_bitstring="100"
            )
        self.assertEqual(output, "110")
