import unittest
import numpy as np

from quantestpy import TestCircuit


class TestTestCircuitCU1Gate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_test_circuit_cu1_gate
    ........
    ----------------------------------------------------------------------
    Ran 7 tests in 0.007s

    OK
    $
    """

    def test_cu1_regular_qubit_order(self,):
        circ = TestCircuit(2)
        lambda_ = np.pi/8
        actual_gate = circ._create_all_qubit_gate_from_cu1_gate(
            control_qubit=[0], target_qubit=[1], control_value=[1],
            parameter=[lambda_]
        )

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, np.exp(1j*lambda_)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu1_qiskit_qubit_order(self,):
        circ = TestCircuit(2)
        lambda_ = np.pi/8
        circ._from_right_to_left_for_qubit_ids = True
        actual_gate = circ._create_all_qubit_gate_from_cu1_gate(
            control_qubit=[0], target_qubit=[1], control_value=[1],
            parameter=[lambda_]
        )

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, np.exp(1j*lambda_)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu1_flip_control_target(self,):
        circ = TestCircuit(2)
        lambda_ = np.pi/8
        actual_gate = circ._create_all_qubit_gate_from_cu1_gate(
            control_qubit=[1], target_qubit=[0], control_value=[1],
            parameter=[lambda_]
        )

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, np.exp(1j*lambda_)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu1_three_qubits_qiskit_qubit_order(self,):
        circ = TestCircuit(3)
        lambda_ = np.pi/8
        circ._from_right_to_left_for_qubit_ids = True
        actual_gate = circ._create_all_qubit_gate_from_cu1_gate(
            control_qubit=[0], target_qubit=[2], control_value=[1],
            parameter=[lambda_]
        )

        # this is qiskit's output
        expected_gate = np.array(
            [[1. + 0.j, 0. + 0.j,
              0. + 0.j, 0. + 0.j,
              0. + 0.j, 0. + 0.j,
              0. + 0.j, 0. + 0.j],
             [0. + 0.j, 1. + 0.j,
                0. + 0.j, 0. + 0.j,
                0. + 0.j, 0. + 0.j,
                0. + 0.j, 0. + 0.j],
                [0. + 0.j, 0. + 0.j,
                 1. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j],
                [0. + 0.j, 0. + 0.j,
                 0. + 0.j, 1. + 0.j,
                 0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j],
                [0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j,
                 1. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j],
                [0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0.92387953+0.38268343j,
                 0. + 0.j, 0. + 0.j],
                [0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j,
                 1. + 0.j, 0. + 0.j],
                [0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0. + 0.j,
                 0. + 0.j, 0.92387953+0.38268343j]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu1_control_value_is_zero(self,):
        circ = TestCircuit(2)
        lambda_ = np.pi/8
        actual_gate = circ._create_all_qubit_gate_from_cu1_gate(
            control_qubit=[0], target_qubit=[1], control_value=[0],
            parameter=[lambda_]
        )

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, np.exp(1j*lambda_), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu1_multiple_controls(self,):
        circ = TestCircuit(3)
        lambda_ = np.pi/8
        actual_gate = circ._create_all_qubit_gate_from_cu1_gate(
            control_qubit=[0, 1], target_qubit=[2], control_value=[1, 1],
            parameter=[lambda_]
        )

        expected_gate = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 1, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 1, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 1, 0],
                                  [0, 0, 0, 0, 0, 0, 0, np.exp(1j*lambda_)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cu1_multiple_targets(self,):
        lambda_ = np.pi/8

        circ = TestCircuit(3)
        gate_0 = circ._create_all_qubit_gate_from_cu1_gate(
            control_qubit=[0], target_qubit=[1, 2], control_value=[1],
            parameter=[lambda_]
        )

        circ = TestCircuit(3)
        gate_1_0 = circ._create_all_qubit_gate_from_cu1_gate(
            control_qubit=[0], target_qubit=[1], control_value=[1],
            parameter=[lambda_]
        )
        gate_1_1 = circ._create_all_qubit_gate_from_cu1_gate(
            control_qubit=[0], target_qubit=[2], control_value=[1],
            parameter=[lambda_]
        )

        self.assertIsNone(
            np.testing.assert_allclose(gate_0, np.matmul(gate_1_0, gate_1_1)))
