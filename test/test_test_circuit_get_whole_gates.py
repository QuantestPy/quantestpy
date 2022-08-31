import unittest
import numpy as np

from quantestpy import TestCircuit


class TestTestCircuitGetWholeGates(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_test_circuit_get_whole_gates
    ........
    ----------------------------------------------------------------------
    Ran 24 tests in 0.009s

    OK
    $
    """
    """
    def test_get_whole_gates(self,):
        _IMPLEMENTED_SINGLE_QUBIT_GATES_WITHOUT_PARAM = [
            "id", "x", "y", "z", "h", "s", "sdg", "t", "tdg"]
        _IMPLEMENTED_SINGLE_QUBIT_GATES_WITH_PARAM = [
            "rx", "ry", "rz", "u1", "u2", "u3"]
        _IMPLEMENTED_MULTIPLE_QUBIT_GATES_WITHOUT_PARAM = [
            "cx", "cy", "cz", "ch"]
        _IMPLEMENTED_MULTIPLE_QUBIT_GATES_WITH_PARAM = [
            "crx", "cry", "crz", "cu1", "cu3"]
        _IMPLEMENTED_SINGLE_QUBIT_GATES = \
            _IMPLEMENTED_SINGLE_QUBIT_GATES_WITHOUT_PARAM \
            + _IMPLEMENTED_SINGLE_QUBIT_GATES_WITH_PARAM
        _IMPLEMENTED_MULTIPLE_QUBIT_GATES = \
            _IMPLEMENTED_MULTIPLE_QUBIT_GATES_WITHOUT_PARAM \
            + _IMPLEMENTED_MULTIPLE_QUBIT_GATES_WITH_PARAM
        _IMPLEMENTED_GATES = _IMPLEMENTED_SINGLE_QUBIT_GATES \
            + _IMPLEMENTED_MULTIPLE_QUBIT_GATES

        for gate in _IMPLEMENTED_GATES:
            if gate == "id":
                circ = TestCircuit(2)
                circ.add_gate()
    """

    def test_get_whole_gates_id(self,):
        circ = TestCircuit(2)
        circ.add_gate(
            {"name": "id", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_x(self,):
        circ = TestCircuit(2)
        circ.add_gate(
            {"name": "x", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[0, 1, 0, 0],
                                  [1, 0, 0, 0],
                                  [0, 0, 0, 1],
                                  [0, 0, 1, 0]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_y(self,):
        circ = TestCircuit(2)
        circ.add_gate(
            {"name": "y", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[0, -1j, 0, 0],
                                  [1j, 0, 0, 0],
                                  [0, 0, 0, -1j],
                                  [0, 0, 1j, 0]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_z(self,):
        circ = TestCircuit(2)
        circ.add_gate(
            {"name": "z", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, -1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, -1]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_h(self,):
        circ = TestCircuit(2)
        circ.add_gate(
            {"name": "h", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1/np.sqrt(2), 1/np.sqrt(2), 0, 0],
                                  [1/np.sqrt(2), -1/np.sqrt(2), 0, 0],
                                  [0, 0, 1/np.sqrt(2), 1/np.sqrt(2)],
                                  [0, 0, 1/np.sqrt(2), -1/np.sqrt(2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_s(self,):
        circ = TestCircuit(2)
        circ.add_gate(
            {"name": "s", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1j, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1j]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_sdg(self,):
        circ = TestCircuit(2)
        circ.add_gate(
            {"name": "sdg", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, -1j, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, -1j]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_t(self,):
        circ = TestCircuit(2)
        circ.add_gate(
            {"name": "t", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, np.exp(1j*np.pi/4), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, np.exp(1j*np.pi/4)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_tdg(self,):
        circ = TestCircuit(2)
        circ.add_gate(
            {"name": "tdg", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, np.exp(-1j*np.pi/4), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, np.exp(-1j*np.pi/4)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_rx(self,):
        circ = TestCircuit(2)
        theta = np.pi/4
        circ.add_gate(
            {"name": "rx", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": [theta]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array(
            [[np.cos(theta/2), -1j*np.sin(theta/2), 0, 0],
             [-1j*np.sin(theta/2), np.cos(theta/2), 0, 0],
             [0, 0, np.cos(theta/2), -1j*np.sin(theta/2)],
             [0, 0, -1j*np.sin(theta/2), np.cos(theta/2)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_ry(self,):
        circ = TestCircuit(2)
        theta = np.pi/4
        circ.add_gate(
            {"name": "ry", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": [theta]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[np.cos(theta/2), -np.sin(theta/2), 0, 0],
                                  [np.sin(theta/2), np.cos(theta/2), 0, 0],
                                  [0, 0, np.cos(theta/2), -np.sin(theta/2)],
                                  [0, 0, np.sin(theta/2), np.cos(theta/2)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_rz(self,):
        circ = TestCircuit(2)
        lambda_ = np.pi/4
        circ.add_gate(
            {"name": "rz", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": [lambda_]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[np.exp(-1j*lambda_/2), 0, 0, 0],
                                  [0, np.exp(1j*lambda_/2), 0, 0],
                                  [0, 0, np.exp(-1j*lambda_/2), 0],
                                  [0, 0, 0, np.exp(1j*lambda_/2)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_u1(self,):
        circ = TestCircuit(2)
        lambda_ = np.pi/4
        circ.add_gate(
            {"name": "u1", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": [lambda_]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, np.exp(1j*lambda_), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, np.exp(1j*lambda_)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_u2(self,):
        circ = TestCircuit(2)
        phi = np.pi/8
        lambda_ = np.pi/4
        circ.add_gate(
            {"name": "u2", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": [phi, lambda_]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1/np.sqrt(2),
                                   -np.exp(1j*lambda_)/np.sqrt(2), 0, 0],
                                  [np.exp(1j*phi)/np.sqrt(2),
                                   np.exp(1j*(lambda_+phi))/np.sqrt(2), 0, 0],
                                  [0, 0, 1/np.sqrt(2),
                                   -np.exp(1j*lambda_)/np.sqrt(2)],
                                  [0, 0, np.exp(1j*phi)/np.sqrt(2),
                                   np.exp(1j*(lambda_+phi))/np.sqrt(2)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_u3(self,):
        circ = TestCircuit(2)
        theta = np.pi/16
        phi = np.pi/8
        lambda_ = np.pi/4
        circ.add_gate(
            {"name": "u3", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": [theta, phi, lambda_]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[np.cos(theta/2),
                                   -np.exp(1j*lambda_)*np.sin(theta/2), 0, 0],
                                  [np.exp(1j*phi)*np.sin(theta/2),
                                   np.exp(1j*(lambda_+phi))*np.cos(theta/2),
                                   0, 0],
                                  [0, 0, np.cos(theta/2),
                                   -np.exp(1j*lambda_)*np.sin(theta/2)],
                                  [0, 0, np.exp(1j*phi)*np.sin(theta/2),
                                   np.exp(1j*(lambda_+phi))*np.cos(theta/2)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_cx(self,):
        circ = TestCircuit(2)
        circ.add_gate(
            {"name": "cx", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 0, 1],
                                  [0, 0, 1, 0]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))
