import unittest

from quantestpy import TestCircuit
from quantestpy import circuit
from quantestpy.exceptions import QuantestPyAssertionError


class TestCircuitAssertIsZero(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_circuit_assert_is_zero
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.006s

    OK
    """

    def test_regular_1(self,):
        test_circuit = TestCircuit(3)
        test_circuit.add_gate(
            {"name": "h", "target_qubit": [0], "control_qubit": [],
             "control_value": []}
        )
        test_circuit.add_gate(
            {"name": "x", "target_qubit": [2], "control_qubit": [],
             "control_value": []}
        )

        self.assertIsNone(
            circuit.assert_is_zero(
                test_circuit=test_circuit,
                qubits=[1]
            )
        )

    def test_regular_2(self,):
        test_circuit = TestCircuit(4)
        test_circuit.add_gate(
            {"name": "h", "target_qubit": [3], "control_qubit": [],
             "control_value": []}
        )
        test_circuit.add_gate(
            {"name": "cx", "target_qubit": [0], "control_qubit": [3],
             "control_value": [1]}
        )

        self.assertIsNone(
            circuit.assert_is_zero(
                test_circuit=test_circuit,
                qubits=[1, 2]
            )
        )

    def test_irregular_1(self,):
        test_circuit = TestCircuit(2)
        test_circuit.add_gate(
            {"name": "h", "target_qubit": [0], "control_qubit": [],
             "control_value": []}
        )
        test_circuit.add_gate(
            {"name": "cx", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1]}
        )

        with self.assertRaises(QuantestPyAssertionError):
            circuit.assert_is_zero(
                test_circuit=test_circuit
            )