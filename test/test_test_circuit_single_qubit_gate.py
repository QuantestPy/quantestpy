import unittest
import numpy as np

from quantestpy import TestCircuit
from quantestpy import test_circuit


class TestTestCircuitSingleQubitGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_test_circuit_single_qubit_gate

    ........
    ----------------------------------------------------------------------
    Ran 4 tests in 0.009s

    OK
    $
    """

    def test_h_to_0_in_qubit_2(self,):
        h = test_circuit._H
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            gate=h, control_qubit=[], target_qubit=[0], control_value=[]
        )

        expected_gate = np.array([[1, 0, 1, 0],
                                  [0, 1, 0, 1],
                                  [1, 0, -1, 0],
                                  [0, 1, 0, -1]]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_h_to_1_in_qubit_2(self,):
        h = test_circuit._H
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            gate=h, control_qubit=[], target_qubit=[1], control_value=[]
        )

        expected_gate = np.array([[1, 1, 0, 0],
                                  [1, -1, 0, 0],
                                  [0, 0, 1, 1],
                                  [0, 0, 1, -1]]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_x_to_0_and_1_in_qubit_2(self,):
        x = test_circuit._X
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            gate=x, control_qubit=[], target_qubit=[0, 1], control_value=[]
        )

        expected_gate = np.array([[0, 0, 0, 1],
                                  [0, 0, 1, 0],
                                  [0, 1, 0, 0],
                                  [1, 0, 0, 0]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_h_to_0_and_1_in_qubit_3_qiskit_convention(self,):
        h = test_circuit._H
        circ = TestCircuit(3)
        circ._from_right_to_left_for_qubit_ids = True
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            gate=h, control_qubit=[], target_qubit=[0, 1], control_value=[]
        )

        # This is a qiskit's output
        expected_gate = np.array(
            [[0.5, 0.5, 0.5, 0.5, 0., 0., 0., 0.],
             [0.5, -0.5, 0.5, -0.5, 0., 0., 0., 0.],
             [0.5, 0.5, -0.5, -0.5, 0., 0., 0., 0.],
             [0.5, -0.5, -0.5, 0.5, 0., 0., 0., 0.],
             [0., 0., 0., 0., 0.5, 0.5, 0.5, 0.5],
             [0., 0., 0., 0., 0.5, -0.5, 0.5, -0.5],
             [0., 0., 0., 0., 0.5, 0.5, -0.5, -0.5],
             [0., 0., 0., 0., 0.5, -0.5, -0.5, 0.5]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))
