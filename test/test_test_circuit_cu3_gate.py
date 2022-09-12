import unittest
import numpy as np

from quantestpy import TestCircuit


class TestTestCircuitCU3Gate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_test_circuit_cu3_gate
    ........
    ----------------------------------------------------------------------
    Ran 7 tests in 0.007s

    OK
    $
    """

    def _u3(self, parameter: list) -> np.ndarray:
        theta, phi, lambda_ = parameter
        return np.array([
            [np.cos(theta/2), -np.exp(1j*lambda_) * np.sin(theta/2)],
            [np.exp(1j*phi)*np.sin(theta/2),
             np.exp(1j*(lambda_ + phi))*np.cos(theta/2)]])

    def test_cu3_regular_qubit_order(self,):
        circ = TestCircuit(2)
        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            self._u3([theta, phi, lambda_]),
            control_qubit=[0], target_qubit=[1], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, np.cos(theta/2), -np.exp(1j*lambda_) * np.sin(theta/2)],
            [0, 0, np.exp(1j*phi)*np.sin(theta/2),
             np.exp(1j*(lambda_ + phi))*np.cos(theta/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu3_qiskit_qubit_order(self,):
        circ = TestCircuit(2)
        circ._from_right_to_left_for_qubit_ids = True
        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            self._u3([theta, phi, lambda_]),
            control_qubit=[0], target_qubit=[1], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, np.cos(theta/2), 0, -np.exp(1j*lambda_) * np.sin(theta/2)],
            [0, 0, 1, 0],
            [0, np.exp(1j*phi)*np.sin(theta/2), 0,
             np.exp(1j*(lambda_ + phi))*np.cos(theta/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu3_flip_control_target(self,):
        circ = TestCircuit(2)
        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            self._u3([theta, phi, lambda_]),
            control_qubit=[1], target_qubit=[0], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, np.cos(theta/2), 0, -np.exp(1j*lambda_) * np.sin(theta/2)],
            [0, 0, 1, 0],
            [0, np.exp(1j*phi)*np.sin(theta/2), 0,
             np.exp(1j*(lambda_ + phi))*np.cos(theta/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu3_three_qubits_qiskit_qubit_order(self,):
        circ = TestCircuit(3)
        circ._from_right_to_left_for_qubit_ids = True
        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            self._u3([theta, phi, lambda_]),
            control_qubit=[0], target_qubit=[2], control_value=[1])

        # this is qiskit's output
        expected_gate = np.array(
            [[1. + 0.j,  0. + 0.j,
              0. + 0.j,  0. + 0.j,
              0. + 0.j,  0. + 0.j,
              0. + 0.j,  0. + 0.j],
             [0. + 0.j,  0.92387953+0.j,
                0. + 0.j,  0. + 0.j,
                0. + 0.j, -0.37533028-0.07465783j,
                0. + 0.j,  0. + 0.j],
             [0. + 0.j,  0. + 0.j,
                1. + 0.j,  0. + 0.j,
                0. + 0.j,  0. + 0.j,
                0. + 0.j,  0. + 0.j],
                [0. + 0.j,  0. + 0.j,
                 0. + 0.j,  0.92387953+0.j,
                 0. + 0.j,  0. + 0.j,
                 0. + 0.j, -0.37533028-0.07465783j],
                [0. + 0.j,  0. + 0.j,
                 0. + 0.j,  0. + 0.j,
                 1. + 0.j,  0. + 0.j,
                 0. + 0.j,  0. + 0.j],
                [0. + 0.j,  0.35355339+0.14644661j,
                 0. + 0.j,  0. + 0.j,
                 0. + 0.j,  0.76817776+0.51327997j,
                 0. + 0.j,  0. + 0.j],
                [0. + 0.j,  0. + 0.j,
                 0. + 0.j,  0. + 0.j,
                 0. + 0.j,  0. + 0.j,
                 1. + 0.j,  0. + 0.j],
                [0. + 0.j,  0. + 0.j,
                 0. + 0.j,  0.35355339+0.14644661j,
                 0. + 0.j,  0. + 0.j,
                 0. + 0.j,  0.76817776+0.51327997j]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu3_control_value_is_zero(self,):
        circ = TestCircuit(2)
        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            self._u3([theta, phi, lambda_]),
            control_qubit=[0], target_qubit=[1], control_value=[0])

        expected_gate = np.array([
            [np.cos(theta/2), -np.exp(1j*lambda_) * np.sin(theta/2), 0, 0],
            [np.exp(1j*phi)*np.sin(theta/2),
             np.exp(1j*(lambda_ + phi))*np.cos(theta/2), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu3_multiple_controls(self,):
        circ = TestCircuit(3)
        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            self._u3([theta, phi, lambda_]),
            control_qubit=[0, 1], target_qubit=[2], control_value=[1, 1])

        expected_gate = np.array(
            [[1, 0, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 0],
             [0, 0, 0, 0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0, 1, 0, 0],
             [0, 0, 0, 0, 0, 0, np.cos(theta/2),
              -np.exp(1j*lambda_) * np.sin(theta/2)],
             [0, 0, 0, 0, 0, 0, np.exp(1j*phi)*np.sin(theta/2),
             np.exp(1j*(lambda_ + phi))*np.cos(theta/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu3_multiple_targets(self,):
        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16

        circ = TestCircuit(3)
        gate_0 = circ._create_all_qubit_gate_from_original_qubit_gate(
            self._u3([theta, phi, lambda_]),
            control_qubit=[0], target_qubit=[1, 2], control_value=[1])

        circ = TestCircuit(3)
        gate_1_0 = circ._create_all_qubit_gate_from_original_qubit_gate(
            self._u3([theta, phi, lambda_]),
            control_qubit=[0], target_qubit=[1], control_value=[1])
        gate_1_1 = circ._create_all_qubit_gate_from_original_qubit_gate(
            self._u3([theta, phi, lambda_]),
            control_qubit=[0], target_qubit=[2], control_value=[1])

        self.assertIsNone(
            np.testing.assert_allclose(gate_0, np.matmul(gate_1_0, gate_1_1)))
