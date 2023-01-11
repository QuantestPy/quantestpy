import unittest

import numpy as np

from quantestpy import StateVectorCircuit
from quantestpy.simulator.state_vector_circuit import _r


class TestStateVectorCircuitCRGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.state_vector_circuit.test_cr_gate
    ......
    ----------------------------------------------------------------------
    Ran 6 tests in 0.020s

    OK
    $
    """

    def test_cr_regular_qubit_order(self,):
        circ = StateVectorCircuit(2)
        theta = np.pi/8
        phi = np.pi/16

        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _r([theta, phi]),
            control_qubit=[0], target_qubit=[1], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, np.cos(theta/2), -1j*np.exp(-1j*phi)*np.sin(theta/2)],
            [0, 0, -1j*np.exp(1j*phi)*np.sin(theta/2), np.cos(theta/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cr_qiskit_qubit_order(self,):
        circ = StateVectorCircuit(2)
        theta = np.pi/8
        phi = np.pi/16

        circ._from_right_to_left_for_qubit_ids = True
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _r([theta, phi]),
            control_qubit=[0], target_qubit=[1], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, np.cos(theta/2), 0, -1j*np.exp(-1j*phi)*np.sin(theta/2)],
            [0, 0, 1, 0],
            [0, -1j*np.exp(1j*phi)*np.sin(theta/2), 0, np.cos(theta/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cr_flip_control_target(self,):
        circ = StateVectorCircuit(2)
        theta = np.pi/8
        phi = np.pi/16

        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _r([theta, phi]),
            control_qubit=[1], target_qubit=[0], control_value=[1])

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, np.cos(theta/2), 0, -1j*np.exp(-1j*phi)*np.sin(theta/2)],
            [0, 0, 1, 0],
            [0, -1j*np.exp(1j*phi)*np.sin(theta/2), 0, np.cos(theta/2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cr_control_value_is_zero(self,):
        circ = StateVectorCircuit(2)
        theta = np.pi/8
        phi = np.pi/16

        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _r([theta, phi]),
            control_qubit=[0], target_qubit=[1], control_value=[0])

        expected_gate = np.array([
            [np.cos(theta/2), -1j*np.exp(-1j*phi)*np.sin(theta/2), 0, 0],
            [-1j*np.exp(1j*phi)*np.sin(theta/2), np.cos(theta/2), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cr_multiple_controls(self,):
        circ = StateVectorCircuit(3)
        theta = np.pi/8
        phi = np.pi/16

        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _r([theta, phi]),
            control_qubit=[0, 1], target_qubit=[2], control_value=[1, 1])

        expected_gate = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0,
                np.cos(theta/2), -1j*np.exp(-1j*phi)*np.sin(theta/2)],
            [0, 0, 0, 0, 0, 0,
                -1j*np.exp(1j*phi)*np.sin(theta/2), np.cos(theta/2)]
        ])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cr_multiple_targets(self,):
        circ = StateVectorCircuit(3)
        theta = np.pi/8
        phi = np.pi/16

        gate_0 = circ._create_all_qubit_gate_from_original_qubit_gate(
            _r([theta, phi]),
            control_qubit=[0], target_qubit=[1, 2], control_value=[1])

        circ = StateVectorCircuit(3)
        gate_1_0 = circ._create_all_qubit_gate_from_original_qubit_gate(
            _r([theta, phi]),
            control_qubit=[0], target_qubit=[1], control_value=[1])
        gate_1_1 = circ._create_all_qubit_gate_from_original_qubit_gate(
            _r([theta, phi]),
            control_qubit=[0], target_qubit=[2], control_value=[1])

        self.assertIsNone(
            np.testing.assert_allclose(gate_0, np.matmul(gate_1_0, gate_1_1)))
