import unittest
import numpy as np

from quantestpy import TestCircuit


class TestTestCircuitCXGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_test_circuit_ch_gate
    ........
    ----------------------------------------------------------------------
    Ran 7 tests in 0.050s

    OK
    $
    """

    def test_ch_regular_qubit_order(self,):
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_ch_gate(
            control_qubit=[0], target_qubit=[1], control_value=[1]
        )

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1/np.sqrt(2), 1/np.sqrt(2)],
                                  [0, 0, 1/np.sqrt(2), -1/np.sqrt(2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_ch_qiskit_qubit_order(self,):
        circ = TestCircuit(2)
        circ._from_right_to_left_for_qubit_ids = True
        actual_gate = circ._create_all_qubit_gate_from_ch_gate(
            control_qubit=[0], target_qubit=[1], control_value=[1]
        )
        # this is qiskit's outputq
        expected_gate = np.array([
            [1. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j],
            [0. + 0.j, 0.70710678 + 0.j, 0. + 0.j, 0.70710678 + 0.j],
            [0. + 0.j, 0. + 0.j, 1. + 0.j, 0. + 0.j],
            [0. + 0.j, 0.70710678+0.j, 0. + 0.j, -0.70710678+0.j]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_ch_flip_control_target(self,):
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_ch_gate(
            control_qubit=[1], target_qubit=[0], control_value=[1]
        )

        # this is qiskit's output
        expected_gate = np.array([
            [1. + 0.j, 0. + 0.j, 0. + 0.j, 0. + 0.j],
            [0. + 0.j, 0.70710678 + 0.j, 0. + 0.j, 0.70710678 + 0.j],
            [0. + 0.j, 0. + 0.j, 1. + 0.j, 0. + 0.j],
            [0. + 0.j, 0.70710678+0.j, 0. + 0.j, -0.70710678+0.j]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_ch_three_qubits_qiskit_qubit_order(self,):
        circ = TestCircuit(3)
        circ._from_right_to_left_for_qubit_ids = True
        actual_gate = circ._create_all_qubit_gate_from_ch_gate(
            control_qubit=[0], target_qubit=[2], control_value=[1]
        )

        # this is qiskit's output
        expected_gate = np.array([[1. + 0.j,  0. + 0.j,  0. + 0.j,
                                   0. + 0.j,  0. + 0.j,  0. + 0.j,
                                   0. + 0.j,  0. + 0.j],
                                  [0. + 0.j,  0.70710678+0.j,  0. + 0.j,
                                   0. + 0.j,  0. + 0.j,  0.70710678+0.j,
                                   0. + 0.j,  0. + 0.j],
                                  [0. + 0.j,  0. + 0.j,  1. + 0.j,
                                   0. + 0.j,  0. + 0.j,  0. + 0.j,
                                   0. + 0.j,  0. + 0.j],
                                  [0. + 0.j,  0. + 0.j,  0. + 0.j,
                                   0.70710678+0.j,  0. + 0.j,  0. + 0.j,
                                   0. + 0.j,  0.70710678+0.j],
                                  [0. + 0.j,  0. + 0.j,  0. + 0.j,
                                   0. + 0.j,  1. + 0.j,  0. + 0.j,
                                   0. + 0.j,  0. + 0.j],
                                  [0. + 0.j,  0.70710678+0.j,  0. + 0.j,
                                   0. + 0.j,  0. + 0.j, -0.70710678+0.j,
                                   0. + 0.j,  0. + 0.j],
                                  [0. + 0.j,  0. + 0.j,  0. + 0.j,
                                   0. + 0.j,  0. + 0.j,  0. + 0.j,
                                   1. + 0.j,  0. + 0.j],
                                  [0. + 0.j,  0. + 0.j,  0. + 0.j,
                                   0.70710678+0.j,  0. + 0.j,  0. + 0.j,
                                   0. + 0.j, -0.70710678+0.j]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_ch_control_value_is_zero(self,):
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_ch_gate(
            control_qubit=[0], target_qubit=[1], control_value=[0]
        )

        expected_gate = np.array([[1/np.sqrt(2), 1/np.sqrt(2), 0, 0],
                                  [1/np.sqrt(2), -1/np.sqrt(2), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_ch_multiple_controls(self,):
        circ = TestCircuit(3)
        actual_gate = circ._create_all_qubit_gate_from_ch_gate(
            control_qubit=[0, 1], target_qubit=[2], control_value=[1, 1]
        )

        expected_gate = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 1, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 1, 0, 0],
                                  [0, 0, 0, 0, 0, 0,
                                   1/np.sqrt(2), 1/np.sqrt(2)],
                                  [0, 0, 0, 0, 0, 0,
                                   1/np.sqrt(2), -1/np.sqrt(2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_ch_multiple_targets(self,):

        circ = TestCircuit(3)
        gate_0 = circ._create_all_qubit_gate_from_ch_gate(
            control_qubit=[0], target_qubit=[1, 2], control_value=[1]
        )

        circ = TestCircuit(3)
        gate_1_0 = circ._create_all_qubit_gate_from_ch_gate(
            control_qubit=[0], target_qubit=[1], control_value=[1]
        )
        gate_1_1 = circ._create_all_qubit_gate_from_ch_gate(
            control_qubit=[0], target_qubit=[2], control_value=[1]
        )

        self.assertIsNone(
            np.testing.assert_allclose(gate_0, np.matmul(gate_1_0, gate_1_1)))
