import unittest
import numpy as np

from quantestpy import TestCircuit


class TestTestCircuitCRXGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_test_circuit_crx_gate
    ........
    ----------------------------------------------------------------------
    Ran 7 tests in 0.007s

    OK
    $
    """
    def _u3(parameter: list) -> np.ndarray:
        theta, phi, lambda_ = parameter
        return np.array([
            [np.cos(theta/2), -np.exp(1j*lambda_) * np.sin(theta/2)],
            [np.exp(1j*phi)*np.sin(theta/2),
             np.exp(1j*(lambda_ + phi))*np.cos(theta/2)]])

    def _rx(parameter: list) -> np.ndarray:
        theta = parameter[0]
        return _u3([theta, -np.pi/2, np.pi/2])

    def test_crx_regular_qubit_order(self,):
        circ = TestCircuit(2)
        lambda_ = np.pi/8
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _rx([lambda_]),
            control_qubit=[0], target_qubit=[1], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, np.cos(lambda_/2), -1j*np.sin(lambda_/2)],
            [0, 0, -1j*np.sin(lambda_/2), np.cos(lambda_/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate,
                                       atol=1e-07))

    def test_crx_qiskit_qubit_order(self,):
        circ = TestCircuit(2)
        lambda_ = np.pi/8
        circ._from_right_to_left_for_qubit_ids = True
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _rx([lambda_]),
            control_qubit=[0], target_qubit=[1], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, np.cos(lambda_/2), 0, -1j*np.sin(lambda_/2)],
            [0, 0, 1, 0],
            [0, - 1j*np.sin(lambda_/2), 0, np.cos(lambda_/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate,
                                       atol=1e-07))

    def test_crx_flip_control_target(self,):
        circ = TestCircuit(2)
        lambda_ = np.pi/8
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _rx([lambda_]),
            control_qubit=[1], target_qubit=[0], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, np.cos(lambda_/2), 0, -1j*np.sin(lambda_/2)],
            [0, 0, 1, 0],
            [0, - 1j*np.sin(lambda_/2), 0, np.cos(lambda_/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate,
                                       atol=1e-07))

    def test_crx_three_qubits_qiskit_qubit_order(self,):
        circ = TestCircuit(3)
        lambda_ = np.pi/8
        circ._from_right_to_left_for_qubit_ids = True
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _rx([lambda_]),
            control_qubit=[0], target_qubit=[2], control_value=[1])

        # this is qiskit's output
        expected_gate = np.array(
            [[1. + 0.j, 0. + 0.j,
              0. + 0.j, 0. + 0.j,
              0. + 0.j, 0. + 0.j,
              0. + 0.j, 0. + 0.j],
             [0. + 0.j, 0.98078528+0.j,
                0. + 0.j, 0. + 0.j,
                0. + 0.j, 0. - 0.19509032j,
              0. + 0.j, 0. + 0.j],
             [0. + 0.j, 0. + 0.j,
                1. + 0.j, 0. + 0.j,
                0. + 0.j, 0. + 0.j,
                0. + 0.j, 0. + 0.j],
                [0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0.98078528+0.j,
                 0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. - 0.19509032j],
                [0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j,
                 1. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j],
                [0. + 0.j, 0. - 0.19509032j,
                 0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0.98078528+0.j,
                 0. + 0.j, 0. + 0.j],
                [0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j,
                 1. + 0.j, 0. + 0.j],
                [0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. - 0.19509032j,
                 0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0.98078528+0.j]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate,
                                       atol=1e-07))

    def test_crx_control_value_is_zero(self,):
        circ = TestCircuit(2)
        lambda_ = np.pi/8
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _rx([lambda_]),
            control_qubit=[0], target_qubit=[1], control_value=[0])

        expected_gate = np.array([
            [np.cos(lambda_/2), -1j*np.sin(lambda_/2), 0, 0],
            [-1j*np.sin(lambda_/2), np.cos(lambda_/2), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate,
                                       atol=1e-07))

    def test_crx_multiple_controls(self,):
        circ = TestCircuit(3)
        lambda_ = np.pi/8
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _rx([lambda_]),
            control_qubit=[0, 1], target_qubit=[2], control_value=[1, 1])

        expected_gate = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 1, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 1, 0, 0],
                                  [0, 0, 0, 0, 0, 0,
                                   np.cos(lambda_/2), -1j*np.sin(lambda_/2)],
                                  [0, 0, 0, 0, 0, 0,
                                   -1j*np.sin(lambda_/2), np.cos(lambda_/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate,
                                       atol=1e-07))

    def test_crx_multiple_targets(self,):
        lambda_ = np.pi/8

        circ = TestCircuit(3)
        gate_0 = circ._create_all_qubit_gate_from_original_qubit_gate(
            _rx([lambda_]),
            control_qubit=[0], target_qubit=[1, 2], control_value=[1])

        circ = TestCircuit(3)
        gate_1_0 = circ._create_all_qubit_gate_from_original_qubit_gate(
            _rx([lambda_]),
            control_qubit=[0], target_qubit=[1], control_value=[1])
        gate_1_1 = circ._create_all_qubit_gate_from_original_qubit_gate(
            _rx([lambda_]),
            control_qubit=[0], target_qubit=[2], control_value=[1])

        self.assertIsNone(
            np.testing.assert_allclose(gate_0, np.matmul(gate_1_0, gate_1_1),
                                       atol=1e-07))
