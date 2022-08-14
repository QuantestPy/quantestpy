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

    def test__create_all_qubit_gate_from_single_qubit_gate_1(self,):
        h = test_circuit._H
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_single_qubit_gate(
            single_qubit_gate=h, target=0
        )

        expected_gate = np.array([[1, 0, 1, 0],
                                  [0, 1, 0, 1],
                                  [1, 0, -1, 0],
                                  [0, 1, 0, -1]]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test__create_all_qubit_gate_from_single_qubit_gate_2(self,):
        h = test_circuit._H
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_single_qubit_gate(
            single_qubit_gate=h, target=1
        )

        expected_gate = np.array([[1, 1, 0, 0],
                                  [1, -1, 0, 0],
                                  [0, 0, 1, 1],
                                  [0, 0, 1, -1]]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test__get_state_vector_1(self,):
        circ = TestCircuit(2)
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([1, 0, 0, 0])

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test__get_state_vector_2(self,):
        circ = TestCircuit(2)
        circ.add_gate({"name": "h", "target_qubit": 0, "control_value": []})
        circ.add_gate({"name": "cnot", "control_qubit": 0, "target_qubit": 1,
                       "control_value": [1]})
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([1, 0, 0, 1]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test__get_state_vector_3(self,):
        circ = TestCircuit(2)
        circ.add_gate({"name": "x", "target_qubit": 0, "control_value": []})
        circ.add_gate({"name": "x", "target_qubit": 1, "control_value": []})
        circ.add_gate({"name": "cnot", "control_qubit": 0, "target_qubit": 1,
                       "control_value": [1]})
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([0, 0, 1, 0])

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test__get_state_vector_4(self,):
        circ = TestCircuit(3)
        circ.add_gate({"name": "x", "target_qubit": 0, "control_value": []})
        circ.add_gate({"name": "cx", "control_qubit": 0, "target_qubit": 2,
                       "control_value": [1]})
        circ.add_gate({"name": "h", "target_qubit": 0, "control_value": []})
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([0, 1, 0, 0, 0, -1, 0, 0]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test__create_all_qubit_gate_from_cnot_gate_1(self,):
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_cnot_gate(
            control=0, target=1, control_value=1
        )

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 0, 1],
                                  [0, 0, 1, 0]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test__create_all_qubit_gate_from_cnot_gate_2(self,):
        circ = TestCircuit(2)
        circ._from_right_to_left_for_qubit_ids = True
        actual_gate = circ._create_all_qubit_gate_from_cnot_gate(
            control=0, target=1, control_value=1
        )

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 0, 0, 1],
                                  [0, 0, 1, 0],
                                  [0, 1, 0, 0]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test__create_all_qubit_gate_from_cnot_gate_3(self,):
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_cnot_gate(
            control=1, target=0, control_value=1
        )

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 0, 0, 1],
                                  [0, 0, 1, 0],
                                  [0, 1, 0, 0]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test__create_all_qubit_gate_from_cnot_gate_4(self,):
        circ = TestCircuit(3)
        circ._from_right_to_left_for_qubit_ids = True
        actual_gate = circ._create_all_qubit_gate_from_cnot_gate(
            control=0, target=2, control_value=1
        )

        expected_gate = np.array([
            [1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
            [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
            [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
            [0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],
            [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j, 0.+0.j]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test__create_all_qubit_gate_from_cnot_gate_5(self,):
        circ = TestCircuit(2)
        actual_gate = circ._create_all_qubit_gate_from_cnot_gate(
            control=0, target=1, control_value=0
        )

        expected_gate = np.array([[0, 1, 0, 0],
                                  [1, 0, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))
