import unittest

import numpy as np

from quantestpy import StateVectorCircuit


class TestStateVectorCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m \
        unittest test.simulator.state_vector_circuit.test_state_vector_circuit
    ......
    ----------------------------------------------------------------------
    Ran 6 tests in 0.006s

    OK
    $
    """

    def test__get_state_vector_1(self,):
        circ = StateVectorCircuit(2)
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([1, 0, 0, 0])

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test__get_state_vector_2(self,):
        circ = StateVectorCircuit(2)
        circ.add_gate({"name": "h", "target_qubit": [0], "control_qubit": [],
                       "control_value": [], "parameter": []})
        circ.add_gate(
            {"name": "x", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1], "parameter": []})
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([1, 0, 0, 1]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test__get_state_vector_3(self,):
        circ = StateVectorCircuit(2)
        circ.add_gate({"name": "x", "target_qubit": [0], "control_qubit": [],
                       "control_value": [], "parameter": []})
        circ.add_gate({"name": "x", "target_qubit": [1], "control_qubit": [],
                       "control_value": [], "parameter": []})
        circ.add_gate(
            {"name": "x", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1], "parameter": []})
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([0, 0, 1, 0])

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test__get_state_vector_4(self,):
        circ = StateVectorCircuit(3)
        circ.add_gate({"name": "x", "target_qubit": [0], "control_qubit": [],
                       "control_value": [], "parameter": []})
        circ.add_gate(
            {"name": "x", "control_qubit": [0], "target_qubit": [2],
             "control_value": [1], "parameter": []})
        circ.add_gate({"name": "h", "target_qubit": [0], "control_qubit": [],
                       "control_value": [], "parameter": []})
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([0, 1, 0, 0, 0, -1, 0, 0]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test_set_initial_state_vector_1(self,):
        circ = StateVectorCircuit(2)
        init_vec = np.array([1, 1j, -1, -1]) / 2.
        circ.set_initial_state_vector(init_vec)
        actual_vec = circ._get_state_vector()

        expected_vec = init_vec

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))

    def test_set_initial_state_vector_2(self,):
        circ = StateVectorCircuit(2)
        init_vec = np.array([1, 0, 1, 0]) / np.sqrt(2.)
        circ.set_initial_state_vector(init_vec)
        circ.add_gate(
            {"name": "x", "control_qubit": [0], "target_qubit": [1],
             "control_value": [1], "parameter": []})
        actual_vec = circ._get_state_vector()

        expected_vec = np.array([1, 0, 0, 1]) / np.sqrt(2.)

        self.assertIsNone(
            np.testing.assert_allclose(actual_vec, expected_vec))
