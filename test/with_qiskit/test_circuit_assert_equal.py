import traceback
import unittest

import numpy as np
from qiskit import QuantumCircuit

from quantestpy import QuantestPyCircuit, assert_equivalent_circuits
from quantestpy.exceptions import QuantestPyAssertionError, QuantestPyError


class TestCircuitAssertEqual(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.with_qiskit.test_circuit_assert_equal
    ...........
    ----------------------------------------------------------------------
    Ran 11 tests in 0.015s

    OK
    """

    def test_msg_from_wrong_input_type_for_circuit_a(self,):

        circuit_a = np.array([[0, 1], [1, 0]])  # wrong
        circuit_b = QuantestPyCircuit(2)  # correct

        try:
            self.assertIsNotNone(
                assert_equivalent_circuits(
                    circuit_a=circuit_a,
                    circuit_b=circuit_b
                )
            )

        except QuantestPyError as e:

            expected_error_msg = "quantestpy.exceptions.QuantestPyError: " \
                + "Input circuit must be one of " \
                + "the following: " \
                + "qasm, qiskit.QuantumCircuit," \
                + "quri_parts.circuit.NonParametricQuantumCircuit," \
                + "quri_parts.circuit." \
                + "ImmutableBoundParametricQuantumCircuit," \
                + "and QuantestPyCircuit.\n"

            actual_error_msg = \
                traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_msg_from_wrong_input_type_for_circuit_b(self,):

        circuit_a = QuantumCircuit(3)  # correct
        circuit_b = [[0, 1], [1, 0]]  # wrong

        try:
            self.assertIsNotNone(
                assert_equivalent_circuits(
                    circuit_a=circuit_a,
                    circuit_b=circuit_b
                )
            )

        except QuantestPyError as e:

            expected_error_msg = "quantestpy.exceptions.QuantestPyError: " \
                + "Input circuit must be one of " \
                + "the following: " \
                + "qasm, qiskit.QuantumCircuit," \
                + "quri_parts.circuit.NonParametricQuantumCircuit," \
                + "quri_parts.circuit." \
                + "ImmutableBoundParametricQuantumCircuit," \
                + "and QuantestPyCircuit.\n"

            actual_error_msg = \
                traceback.format_exception_only(type(e), e)[0]

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_exact_equal(self,):
        """Check CNOT basis transformation; see Nielsen-Chuang p.179"""
        qc_a = QuantestPyCircuit(2)
        qc_a.add_gate(
            {"name": "h", "target_qubit": [0, 1], "control_qubit": [],
                "control_value": [], "parameter": []}
        )
        qc_a.add_gate(
            {"name": "x", "target_qubit": [1], "control_qubit": [0],
                "control_value": [1], "parameter": []}
        )
        qc_a.add_gate(
            {"name": "h", "target_qubit": [0, 1], "control_qubit": [],
                "control_value": [], "parameter": []}
        )

        qc_b = QuantestPyCircuit(2)
        qc_b.add_gate(
            {"name": "x", "target_qubit": [0], "control_qubit": [1],
                "control_value": [1], "parameter": []}
        )

        self.assertIsNone(
            assert_equivalent_circuits(
                circuit_a=qc_a,
                circuit_b=qc_b
            )
        )

    def test_msg_from_wrong_type_for_atol(self,):

        qc_a = QuantestPyCircuit(2)
        qc_b = QuantestPyCircuit(2)

        test_patterns = [
            1,
            1.+2j,
            np.array([1.], dtype=np.float32)[0]
        ]

        for tolerance in test_patterns:

            try:
                self.assertIsNotNone(
                    assert_equivalent_circuits(
                        circuit_a=qc_a,
                        circuit_b=qc_b,
                        atol=tolerance
                    )
                )

            except QuantestPyError as e:

                expected_error_msg = \
                    "quantestpy.exceptions.QuantestPyError: " \
                    + "Type of atol must be float."

                actual_error_msg = \
                    traceback.format_exception_only(type(e), e)[0].rstrip("\n")

                self.assertEqual(expected_error_msg, actual_error_msg)

    def test_matrix_norms(self,):

        qc_a = QuantestPyCircuit(2)
        qc_a.add_gate(
            {"name": "x", "target_qubit": [0, 1], "control_qubit": [],
                "control_value": [], "parameter": []}
        )
        qc_a.add_gate(
            {"name": "s", "target_qubit": [1], "control_qubit": [],
                "control_value": [], "parameter": []}
        )

        qc_b = QuantestPyCircuit(2)
        qc_b.add_gate(
            {"name": "x", "target_qubit": [0], "control_qubit": [1],
                "control_value": [1], "parameter": []}
        )

        test_patterns = [
            {"matrix_norm_type": "operator_norm_1",
             "atol": 1.,
             "expected_matrix_norm_value": 2.},
            {"matrix_norm_type": "operator_norm_inf",
             "atol": 1.5,
             "expected_matrix_norm_value": 2.},
            {"matrix_norm_type": "Frobenius_norm",
             "atol": 2.,
             "expected_matrix_norm_value": 2.*np.sqrt(2.)},
            {"matrix_norm_type": "max_norm",
             "atol": 0.1,
             "expected_matrix_norm_value": 1.}
        ]

        for pattern in test_patterns:

            try:
                self.assertIsNotNone(
                    assert_equivalent_circuits(
                        circuit_a=qc_a,
                        circuit_b=qc_b,
                        matrix_norm_type=pattern["matrix_norm_type"],
                        atol=pattern["atol"]
                    )
                )

            except QuantestPyAssertionError as e:

                expected_error_msg = \
                    "quantestpy.exceptions.QuantestPyAssertionError: " \
                    + "matrix norm ||A-B|| " \
                    + format(pattern["expected_matrix_norm_value"], ".15g") \
                    + " is larger than (atol + rtol*||B||) " \
                    + format(pattern["atol"], ".15g") \
                    + "."

                actual_error_msg = \
                    traceback.format_exception_only(type(e), e)[0].rstrip("\n")

                self.assertEqual(expected_error_msg, actual_error_msg)

    def test_operator_norm_2(self,):

        qc_a = QuantestPyCircuit(1)
        qc_a.add_gate(
            {"name": "x", "target_qubit": [0], "control_qubit": [],
                "control_value": [], "parameter": []}
        )

        qc_b = QuantestPyCircuit(1)
        qc_b.add_gate(
            {"name": "s", "target_qubit": [0], "control_qubit": [],
                "control_value": [], "parameter": []}
        )

        try:
            self.assertIsNotNone(
                assert_equivalent_circuits(
                    circuit_a=qc_a,
                    circuit_b=qc_b,
                    matrix_norm_type="operator_norm_2",
                    atol=1.5
                )
            )

        except QuantestPyAssertionError as e:

            expected_error_msg = \
                "quantestpy.exceptions.QuantestPyAssertionError: " \
                + "matrix norm ||A-B|| " \
                + format(np.sqrt(2.+np.sqrt(2.)), ".15g") \
                + f" is larger than (atol + rtol*||B||) {1.5}."

            actual_error_msg = \
                traceback.format_exception_only(type(e), e)[0].rstrip("\n")

            self.assertEqual(expected_error_msg, actual_error_msg)

    def test_matrix_norms_with_rtol(self,):

        qc_a = QuantestPyCircuit(2)
        qc_a.add_gate(
            {"name": "x", "target_qubit": [0, 1], "control_qubit": [],
                "control_value": [], "parameter": []}
        )
        qc_a.add_gate(
            {"name": "s", "target_qubit": [1], "control_qubit": [],
                "control_value": [], "parameter": []}
        )

        qc_b = QuantestPyCircuit(2)
        qc_b.add_gate(
            {"name": "x", "target_qubit": [0], "control_qubit": [1],
                "control_value": [1], "parameter": []}
        )

        test_patterns = [
            {"matrix_norm_type": "operator_norm_1",
             "rtol": 1.1,
             "expected_matrix_norm_a_minus_b": 2.,
             "expected_matrix_norm_b": 1.},
            {"matrix_norm_type": "operator_norm_inf",
             "rtol": 1.5,
             "expected_matrix_norm_a_minus_b": 2.,
             "expected_matrix_norm_b": 1.},
            {"matrix_norm_type": "Frobenius_norm",
             "rtol": 1.1,
             "expected_matrix_norm_a_minus_b": 2.*np.sqrt(2.),
             "expected_matrix_norm_b": 2.},
            {"matrix_norm_type": "max_norm",
             "rtol": 0.1,
             "expected_matrix_norm_a_minus_b": 1.,
             "expected_matrix_norm_b": 1.}
        ]

        for pattern in test_patterns:

            try:
                self.assertIsNotNone(
                    assert_equivalent_circuits(
                        circuit_a=qc_a,
                        circuit_b=qc_b,
                        matrix_norm_type=pattern["matrix_norm_type"],
                        atol=0.,
                        rtol=pattern["rtol"]
                    )
                )

            except QuantestPyAssertionError as e:

                expected_error_msg = \
                    "quantestpy.exceptions.QuantestPyAssertionError: " \
                    + "matrix norm ||A-B|| " \
                    + format(pattern["expected_matrix_norm_a_minus_b"],
                             ".15g") \
                    + " is larger than (atol + rtol*||B||) " \
                    + format(pattern["rtol"]
                             * pattern["expected_matrix_norm_b"], ".15g") \
                    + "."

                actual_error_msg = \
                    traceback.format_exception_only(type(e), e)[0].rstrip("\n")

                self.assertEqual(expected_error_msg, actual_error_msg)
