import unittest

from quantestpy.assertion.assert_unary_iteration import _assert_ancilla_reset
from quantestpy.simulator.pauli_circuit import PauliCircuit


class TestAssertInternal(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.assertion.assert_unary_iteration.test_assert_ancilla_reset
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.001s
    OK
    $
    """

    def test_return_none(self):
        pc = PauliCircuit(5)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        pc.add_gate({"name": "y", "control_qubit": [2], "target_qubit": [3],
                    "control_value": [1]})
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})

        self.assertIsNone(
            _assert_ancilla_reset(
                pauli_circuit_org=pc,
                index_reg=[0, 1],
                ancilla_reg=[2],
                in_bitstring="11"
            )
        )

    def test_return_obj(self):
        pc = PauliCircuit(5)
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [1, 1]})
        pc.add_gate({"name": "y", "control_qubit": [2], "target_qubit": [3],
                    "control_value": [1]})
        pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
                    "control_value": [0, 0]})

        output = _assert_ancilla_reset(
            pauli_circuit_org=pc,
            index_reg=[0, 1],
            ancilla_reg=[2],
            in_bitstring="11"
        )
        self.assertEqual(output, [2])
