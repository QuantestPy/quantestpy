import unittest
import traceback
import numpy as np

from quantestpy import TestCircuit
from quantestpy import circuit
from quantestpy.exceptions import QuantestPyError

from qiskit import QuantumCircuit


class TestCircuitAssertEqual(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_circuit_assert_equal
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.006s

    OK
    """

    def test_msg_from_miss_all_info_for_circuit_a(self,):
        test_circuit = TestCircuit(2)

        try:
            self.assertIsNotNone(
                circuit.assert_equal(
                    test_circuit_b=test_circuit
                )
            )

        except QuantestPyError as e:

            expected_error_msg = "quantestpy.exceptions.QuantestPyError: " \
                + "Missing information for circuit A. " \
                + "One of the following must be given: " \
                + "qasm_a, qiskit_circuit_a and test_circuit_a.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_miss_all_info_for_circuit_b(self,):
        test_circuit = TestCircuit(3)

        try:
            self.assertIsNotNone(
                circuit.assert_equal(
                    test_circuit_a=test_circuit
                )
            )

        except QuantestPyError as e:

            expected_error_msg = "quantestpy.exceptions.QuantestPyError: " \
                + "Missing information for circuit B. " \
                + "One of the following must be given: " \
                + "qasm_b, qiskit_circuit_b and test_circuit_b.\n"

            actual_error_msg = traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_too_much_info_for_circuit_a(self,):

        qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[2];\nx q[0];\n'
        qiskit_circuit = QuantumCircuit(2)
        test_circuit = TestCircuit(3)

        test_circuit_b = TestCircuit(2)

        test_patterns = [
            (qasm, None, test_circuit),
            (None, qiskit_circuit, test_circuit),
            (qasm, qiskit_circuit, None),
            (qasm, qiskit_circuit, test_circuit)
        ]

        for _qasm, _qiskit_circuit, _test_circuit in test_patterns:

            try:
                self.assertIsNotNone(
                    circuit.assert_equal(
                        qasm_a=_qasm,
                        qiskit_circuit_a=_qiskit_circuit,
                        test_circuit_a=_test_circuit,
                        test_circuit_b=test_circuit_b
                    )
                )

            except QuantestPyError as e:

                expected_error_msg = \
                    "quantestpy.exceptions.QuantestPyError: " \
                    + "Too much information for circuit A. " \
                    + "Only one of the following should be given: " \
                    + "qasm_a, qiskit_circuit_a and test_circuit_a.\n"

                actual_error_msg = \
                    traceback.format_exception_only(type(e), e)[0]

                self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_too_much_info_for_circuit_b(self,):

        qasm = 'OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[2];\nx q[0];\n'
        qiskit_circuit = QuantumCircuit(2)
        test_circuit = TestCircuit(2)

        test_circuit_a = TestCircuit(2)

        test_patterns = [
            (qasm, None, test_circuit),
            (None, qiskit_circuit, test_circuit),
            (qasm, qiskit_circuit, None),
            (qasm, qiskit_circuit, test_circuit)
        ]

        for _qasm, _qiskit_circuit, _test_circuit in test_patterns:

            try:
                self.assertIsNotNone(
                    circuit.assert_equal(
                        qasm_b=_qasm,
                        qiskit_circuit_b=_qiskit_circuit,
                        test_circuit_b=_test_circuit,
                        test_circuit_a=test_circuit_a
                    )
                )

            except QuantestPyError as e:

                expected_error_msg = \
                    "quantestpy.exceptions.QuantestPyError: " \
                    + "Too much information for circuit B. " \
                    + "Only one of the following should be given: " \
                    + "qasm_b, qiskit_circuit_b and test_circuit_b.\n"

                actual_error_msg = \
                    traceback.format_exception_only(type(e), e)[0]

                self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_wrong_input_type_for_circuit_a(self,):
        qasm = 1  # wrong type
        qiskit_circuit = "hoge"  # wrong type
        test_circuit = QuantumCircuit(2)  # wrong type

        test_circuit_b = TestCircuit(2)

        test_patterns = [
            {"argument": [qasm, None, None],
             "circuit_option": "qasm_a",
             "expected_type": "str"},
            {"argument": [None, qiskit_circuit, None],
             "circuit_option": "qiskit_circuit_a",
             "expected_type": "an instance of qiskit.QuantumCircuit class"},
            {"argument": [None, None, test_circuit],
             "circuit_option": "test_circuit_a",
             "expected_type": "an instance of quantestpy.TestCircuit class"}
        ]

        for pattern in test_patterns:
            _qasm, _qiskit_circuit, _test_circuit = pattern["argument"]

            try:
                self.assertIsNotNone(
                    circuit.assert_equal(
                        qasm_a=_qasm,
                        qiskit_circuit_a=_qiskit_circuit,
                        test_circuit_a=_test_circuit,
                        test_circuit_b=test_circuit_b
                    )
                )

            except QuantestPyError as e:

                expected_error_msg = \
                    "quantestpy.exceptions.QuantestPyError: " \
                    + f'Type of {pattern["circuit_option"]} must be ' \
                    + f'{pattern["expected_type"]}.\n'

                actual_error_msg = \
                    traceback.format_exception_only(type(e), e)[0]

                self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_wrong_input_type_for_circuit_b(self,):
        qasm = QuantumCircuit(2)  # wrong type
        qiskit_circuit = TestCircuit(2)  # wrong type
        test_circuit = 3  # wrong type

        test_circuit_a = TestCircuit(2)

        test_patterns = [
            {"argument": [qasm, None, None],
             "circuit_option": "qasm_b",
             "expected_type": "str"},
            {"argument": [None, qiskit_circuit, None],
             "circuit_option": "qiskit_circuit_b",
             "expected_type": "an instance of qiskit.QuantumCircuit class"},
            {"argument": [None, None, test_circuit],
             "circuit_option": "test_circuit_b",
             "expected_type": "an instance of quantestpy.TestCircuit class"}
        ]

        for pattern in test_patterns:
            _qasm, _qiskit_circuit, _test_circuit = pattern["argument"]

            try:
                self.assertIsNotNone(
                    circuit.assert_equal(
                        qasm_b=_qasm,
                        qiskit_circuit_b=_qiskit_circuit,
                        test_circuit_b=_test_circuit,
                        test_circuit_a=test_circuit_a
                    )
                )

            except QuantestPyError as e:

                expected_error_msg = \
                    "quantestpy.exceptions.QuantestPyError: " \
                    + f'Type of {pattern["circuit_option"]} must be ' \
                    + f'{pattern["expected_type"]}.\n'

                actual_error_msg = \
                    traceback.format_exception_only(type(e), e)[0]

                self.assertEqual(expected_error_msg, actual_error_msg)

    def test_exact_equal(self,):
        """Check CNOT basis transformation; see Nielsen-Chuang p.179"""
        test_circuit_a = TestCircuit(2)
        test_circuit_a.add_gate(
            {"name": "h", "target_qubit": [0, 1], "control_qubit": [],
                "control_value": []}
        )
        test_circuit_a.add_gate(
            {"name": "cx", "target_qubit": [1], "control_qubit": [0],
                "control_value": [1]}
        )
        test_circuit_a.add_gate(
            {"name": "h", "target_qubit": [0, 1], "control_qubit": [],
                "control_value": []}
        )

        test_circuit_b = TestCircuit(2)
        test_circuit_b.add_gate(
            {"name": "cx", "target_qubit": [0], "control_qubit": [1],
                "control_value": [1]}
        )

        self.assertIsNone(
            circuit.assert_equal(
                test_circuit_a=test_circuit_a,
                test_circuit_b=test_circuit_b
            )
        )

    @unittest.skip("Skip until RY gate is implemented.")
    def test_exact_equal_up_to_a_global_phase(self,):
        """Check Toffoli up to a global phase; see Nielsen-Chuang p.183"""
        qc = QuantumCircuit(3)
        qc.ry(theta=np.pi/4., qubit=2)
        qc.cx(1, 2)
        qc.ry(theta=np.pi/4., qubit=2)
        qc.cx(0, 2)
        qc.ry(theta=-np.pi/4., qubit=2)
        qc.cx(1, 2)
        qc.ry(theta=-np.pi/4., qubit=2)

        test_circuit = TestCircuit(3)
        test_circuit.add_gate(
            {"name": "cx", "target_qubit": [2], "control_qubit": [0, 1],
                "control_value": [1, 1]}
        )

        self.assertIsNone(
            circuit.assert_equal(
                qiskit_circuit_a=qc,
                test_circuit_b=test_circuit,
                check_including_global_phase=False
            )
        )