import unittest
import traceback

from quantestpy import TestCircuit
from quantestpy import circuit
from quantestpy.exceptions import QuantestPyAssertionError


class TestCircuitAssertAncillaIsZero(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_circuit_assert_ancilla_is_zero
    ...
    ----------------------------------------------------------------------
    Ran 2 tests in 0.017s

    OK
    """

    def test_regular_1(self,):
        test_circuit = TestCircuit(4)
        # V
        test_circuit.add_gate(
            {"name": "cx", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1], "parameter": []}
        )
        test_circuit.add_gate(
            {"name": "cx", "control_qubit": [1], "target_qubit": [2],
             "control_value": [1], "parameter": []}
        )

        # uncomputation
        test_circuit.add_gate(
            {"name": "cx", "control_qubit": [1], "target_qubit": [3],
             "control_value": [1], "parameter": []}
        )

        # V^{-1}
        test_circuit.add_gate(
            {"name": "cx", "control_qubit": [1], "target_qubit": [2],
             "control_value": [1], "parameter": []}
        )
        test_circuit.add_gate(
            {"name": "cx", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1], "parameter": []}
        )

        self.assertIsNone(
            circuit.assert_ancilla_is_zero(
                test_circuit=test_circuit,
                ancilla_qubits=[1, 2]
            )
        )

    def test_irregular_1(self,):
        test_circuit = TestCircuit(4)
        # V
        test_circuit.add_gate(
            {"name": "cx", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1], "parameter": []}
        )
        test_circuit.add_gate(
            {"name": "cx", "control_qubit": [1], "target_qubit": [2],
             "control_value": [1], "parameter": []}
        )

        # uncomputation
        test_circuit.add_gate(
            {"name": "cx", "control_qubit": [1], "target_qubit": [3],
             "control_value": [1], "parameter": []}
        )

        # V^{-1}: Wrong order!!
        test_circuit.add_gate(
            {"name": "cx", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1], "parameter": []}
        )
        test_circuit.add_gate(
            {"name": "cx", "control_qubit": [1], "target_qubit": [2],
             "control_value": [1], "parameter": []}
        )

        try:
            circuit.assert_ancilla_is_zero(
                test_circuit=test_circuit,
                ancilla_qubits=[1, 2]
            )

        except QuantestPyAssertionError as e:

            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyAssertionError: qubit(s) " \
                + "[2] are either non-zero or entangled with other qubits.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)
