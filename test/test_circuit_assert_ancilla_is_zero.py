import traceback
import unittest

from quantestpy import QuantestPyCircuit, circuit
from quantestpy.exceptions import QuantestPyAssertionError


class TestCircuitAssertAncillaIsZero(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_circuit_assert_ancilla_is_zero
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.135s

    OK
    """

    def test_regular_1(self,):
        qc = QuantestPyCircuit(4)
        # V
        qc.add_gate(
            {"name": "x", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1], "parameter": []}
        )
        qc.add_gate(
            {"name": "x", "control_qubit": [1], "target_qubit": [2],
             "control_value": [1], "parameter": []}
        )

        # uncomputation
        qc.add_gate(
            {"name": "x", "control_qubit": [1], "target_qubit": [3],
             "control_value": [1], "parameter": []}
        )

        # V^{-1}
        qc.add_gate(
            {"name": "x", "control_qubit": [1], "target_qubit": [2],
             "control_value": [1], "parameter": []}
        )
        qc.add_gate(
            {"name": "x", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1], "parameter": []}
        )

        self.assertIsNone(
            circuit.assert_ancilla_is_zero(
                circuit=qc,
                ancilla_qubits=[1, 2]
            )
        )

    def test_irregular_1(self,):
        qc = QuantestPyCircuit(4)
        # V
        qc.add_gate(
            {"name": "x", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1], "parameter": []}
        )
        qc.add_gate(
            {"name": "x", "control_qubit": [1], "target_qubit": [2],
             "control_value": [1], "parameter": []}
        )

        # uncomputation
        qc.add_gate(
            {"name": "x", "control_qubit": [1], "target_qubit": [3],
             "control_value": [1], "parameter": []}
        )

        # V^{-1}: Wrong order!!
        qc.add_gate(
            {"name": "x", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1], "parameter": []}
        )
        qc.add_gate(
            {"name": "x", "control_qubit": [1], "target_qubit": [2],
             "control_value": [1], "parameter": []}
        )

        try:
            self.assertIsNotNone(
                circuit.assert_ancilla_is_zero(
                    circuit=qc,
                    ancilla_qubits=[1, 2]
                )
            )

        except QuantestPyAssertionError as e:

            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyAssertionError: qubit(s) " \
                + "[2] are either non-zero or entangled with other qubits.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)
