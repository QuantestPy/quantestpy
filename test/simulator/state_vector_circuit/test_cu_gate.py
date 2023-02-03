import unittest

import numpy as np

from quantestpy import StateVectorCircuit
from quantestpy.simulator.state_vector_circuit import _u


class TestStateVectorCircuitCUGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.state_vector_circuit.test_cu_gate
    ........
    ----------------------------------------------------------------------
    Ran 7 tests in 0.007s

    OK
    $
    """

    def test_cu_regular_qubit_order(self,):
        circ = StateVectorCircuit(2)

        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        gamma = 0

        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _u([theta, phi, lambda_, gamma]),
            control_qubit=[0], target_qubit=[1], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, np.cos(theta/2), -np.exp(1j*lambda_) * np.sin(theta/2)],
            [0, 0, np.exp(1j*phi)*np.sin(theta/2),
             np.exp(1j*(lambda_ + phi))*np.cos(theta/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu_qiskit_qubit_order(self,):
        circ = StateVectorCircuit(2)
        circ._from_right_to_left_for_qubit_ids = True

        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        gamma = 0

        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _u([theta, phi, lambda_, gamma]),
            control_qubit=[0], target_qubit=[1], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, np.cos(theta/2), 0, -np.exp(1j*lambda_) * np.sin(theta/2)],
            [0, 0, 1, 0],
            [0, np.exp(1j*phi)*np.sin(theta/2), 0,
             np.exp(1j*(lambda_ + phi))*np.cos(theta/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu_flip_control_target(self,):
        circ = StateVectorCircuit(2)

        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        gamma = 0

        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _u([theta, phi, lambda_, gamma]),
            control_qubit=[1], target_qubit=[0], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, np.cos(theta/2), 0, -np.exp(1j*lambda_) * np.sin(theta/2)],
            [0, 0, 1, 0],
            [0, np.exp(1j*phi)*np.sin(theta/2), 0,
             np.exp(1j*(lambda_ + phi))*np.cos(theta/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu_three_qubits_qiskit_qubit_order(self,):
        circ = StateVectorCircuit(3)
        circ._from_right_to_left_for_qubit_ids = True

        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        gamma = 0

        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _u([theta, phi, lambda_, gamma]),
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

    def test_cu_control_value_is_zero(self,):
        circ = StateVectorCircuit(2)

        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        gamma = 0

        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _u([theta, phi, lambda_, gamma]),
            control_qubit=[0], target_qubit=[1], control_value=[0])

        expected_gate = np.array([
            [np.cos(theta/2), -np.exp(1j*lambda_) * np.sin(theta/2), 0, 0],
            [np.exp(1j*phi)*np.sin(theta/2),
             np.exp(1j*(lambda_ + phi))*np.cos(theta/2), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu_multiple_controls(self,):
        circ = StateVectorCircuit(3)

        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        gamma = 0

        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _u([theta, phi, lambda_, gamma]),
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

    def test_cu_multiple_targets(self,):
        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        gamma = 0

        circ = StateVectorCircuit(3)
        gate_0 = circ._create_all_qubit_gate_from_original_qubit_gate(
            _u([theta, phi, lambda_, gamma]),
            control_qubit=[0], target_qubit=[1, 2], control_value=[1])

        circ = StateVectorCircuit(3)
        gate_1_0 = circ._create_all_qubit_gate_from_original_qubit_gate(
            _u([theta, phi, lambda_, gamma]),
            control_qubit=[0], target_qubit=[1], control_value=[1])
        gate_1_1 = circ._create_all_qubit_gate_from_original_qubit_gate(
            _u([theta, phi, lambda_, gamma]),
            control_qubit=[0], target_qubit=[2], control_value=[1])

        self.assertIsNone(
            np.testing.assert_allclose(gate_0, np.matmul(gate_1_0, gate_1_1)))
