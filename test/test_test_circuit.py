import unittest
import numpy as np

from quantestpy import TestCircuit
from quantestpy import test_circuit


class TestTestCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_test_circuit
    ........
    ----------------------------------------------------------------------
    Ran 8 tests in 0.009s

    OK
    $
    """

    def test__calculate_matrix_tensor_prod_1(self,):
        x = test_circuit._X
        h = test_circuit._H
        actual_matrix = TestCircuit._calculate_matrix_tensor_prod(x, h)

        expected_matrix = np.array([[0, 0, 1, 1],
                                   [0, 0, 1, -1],
                                   [1, 1, 0, 0],
                                   [1, -1, 0, 0]]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_matrix, expected_matrix))

    def test__calculate_matrix_tensor_prod_2(self,):
        x = test_circuit._X
        h = test_circuit._H
        actual_matrix = TestCircuit._calculate_matrix_tensor_prod(h, x)

        expected_matrix = np.array([[0, 1, 0, 1],
                                   [1, 0, 1, 0],
                                   [0, 1, 0, -1],
                                   [1, 0, -1, 0]]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_matrix, expected_matrix))

    def test__get_state_vector_1(self,):
        circ = TestCircuit(2)
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([1, 0, 0, 0])

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test__get_state_vector_2(self,):
        circ = TestCircuit(2)
        circ.add_gate({"name": "h", "target_qubit": [0], "control_qubit": [],
                       "control_value": []})
        circ.add_gate(
            {"name": "cx", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1]})
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([1, 0, 0, 1]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test__get_state_vector_3(self,):
        circ = TestCircuit(2)
        circ.add_gate({"name": "x", "target_qubit": [0], "control_qubit": [],
                       "control_value": []})
        circ.add_gate({"name": "x", "target_qubit": [1], "control_qubit": [],
                       "control_value": []})
        circ.add_gate(
            {"name": "cx", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1]})
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([0, 0, 1, 0])

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test__get_state_vector_4(self,):
        circ = TestCircuit(3)
        circ.add_gate({"name": "x", "target_qubit": [0], "control_qubit": [],
                       "control_value": []})
        circ.add_gate(
            {"name": "cx", "control_qubit": [0], "target_qubit": [2],
             "control_value": [1]})
        circ.add_gate({"name": "h", "target_qubit": [0], "control_qubit": [],
                       "control_value": []})
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([0, 1, 0, 0, 0, -1, 0, 0]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test_set_initial_state_vector_1(self,):
        circ = TestCircuit(2)
        init_vec = np.array([1, 1j, -1, -1]) / 2.
        circ.set_initial_state_vector(init_vec)
        actual_vec = circ._get_state_vector()

        expected_vec = init_vec

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test_set_initial_state_vector_2(self,):
        circ = TestCircuit(2)
        init_vec = np.array([1, 0, 1, 0]) / np.sqrt(2.)
        circ.set_initial_state_vector(init_vec)
        circ.add_gate(
            {"name": "cx", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1]})
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([1, 0, 0, 1]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))
