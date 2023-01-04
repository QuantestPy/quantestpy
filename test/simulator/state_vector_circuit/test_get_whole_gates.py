import unittest

import numpy as np

from quantestpy import StateVectorCircuit


class TestStateVectorCircuitGetWholeGates(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m \
        unittest test.simulator.state_vector_circuit.test_get_whole_gates
    ............................
    ----------------------------------------------------------------------
    Ran 28 tests in 0.012s

    OK
    $
    """

    def test_get_whole_gates_id(self,):
        circ = StateVectorCircuit(2)
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
        circ = StateVectorCircuit(2)
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
        circ = StateVectorCircuit(2)
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
        circ = StateVectorCircuit(2)
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
        circ = StateVectorCircuit(2)
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
        circ = StateVectorCircuit(2)
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
        circ = StateVectorCircuit(2)
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
        circ = StateVectorCircuit(2)
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
        circ = StateVectorCircuit(2)
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
        circ = StateVectorCircuit(2)
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
        circ = StateVectorCircuit(2)
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
        circ = StateVectorCircuit(2)
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

    def test_get_whole_gates_p(self,):
        circ = StateVectorCircuit(2)
        lambda_ = np.pi/4
        circ.add_gate(
            {"name": "p", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": [lambda_]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, np.exp(1j*lambda_), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, np.exp(1j*lambda_)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_u(self,):
        circ = StateVectorCircuit(2)
        theta = np.pi/16
        phi = np.pi/8
        lambda_ = np.pi/4
        gamma = 0
        circ.add_gate(
            {"name": "u", "target_qubit": [1], "control_qubit": [],
             "control_value": [], "parameter": [theta, phi, lambda_, gamma]})

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
        circ = StateVectorCircuit(2)
        circ.add_gate(
            {"name": "x", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 0, 1],
                                  [0, 0, 1, 0]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_cy(self,):
        circ = StateVectorCircuit(2)
        circ.add_gate(
            {"name": "y", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 0, -1j],
                                  [0, 0, 1j, 0]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_cz(self,):
        circ = StateVectorCircuit(2)
        circ.add_gate(
            {"name": "z", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, -1]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate, atol=1e-07))

    def test_get_whole_gates_ch(self,):
        circ = StateVectorCircuit(2)
        circ.add_gate(
            {"name": "h", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": []})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1/np.sqrt(2), 1/np.sqrt(2)],
                                  [0, 0, 1/np.sqrt(2), -1/np.sqrt(2)]])

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate, atol=1e-07))

    def test_get_whole_gates_crx(self,):
        circ = StateVectorCircuit(2)
        theta = np.pi/4
        circ.add_gate(
            {"name": "rx", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": [theta]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, np.cos(theta/2), -1j*np.sin(theta/2)],
            [0, 0, -1j*np.sin(theta/2), np.cos(theta/2)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate, atol=1e-07))

    def test_get_whole_gates_cry(self,):
        circ = StateVectorCircuit(2)
        theta = np.pi/4
        circ.add_gate(
            {"name": "ry", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": [theta]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, np.cos(theta/2), -np.sin(theta/2)],
                                  [0, 0, np.sin(theta/2), np.cos(theta/2)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate, atol=1e-07))

    def test_get_whole_gates_crz(self,):
        circ = StateVectorCircuit(2)
        lambda_ = np.pi/4
        circ.add_gate(
            {"name": "rz", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": [lambda_]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, np.exp(-1j*lambda_/2), 0],
                                  [0, 0, 0, np.exp(1j*lambda_/2)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_cp(self,):
        circ = StateVectorCircuit(2)
        lambda_ = np.pi/4
        circ.add_gate(
            {"name": "p", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": [lambda_]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, np.exp(1j*lambda_)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_cu(self,):
        circ = StateVectorCircuit(2)
        theta = np.pi/16
        phi = np.pi/8
        lambda_ = np.pi/4
        gamma = 0
        circ.add_gate(
            {"name": "u", "target_qubit": [1], "control_qubit": [0],
             "control_value": [1], "parameter": [theta, phi, lambda_, gamma]})

        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, np.cos(theta/2),
                                   -np.exp(1j*lambda_)*np.sin(theta/2)],
                                  [0, 0, np.exp(1j*phi)*np.sin(theta/2),
                                   np.exp(1j*(lambda_+phi))*np.cos(theta/2)]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate, atol=1e-07))

    def test_scalar_one_target(self,):

        test_patterns = [
            (0, np.pi/3.),
            (1, np.pi/5.),
            (2, np.pi/7.)
        ]

        for target_qubit, parameter in test_patterns:
            circ = StateVectorCircuit(3)
            circ.add_gate(
                {"name": "scalar",
                 "target_qubit": [target_qubit],
                 "control_qubit": [],
                 "control_value": [],
                 "parameter": [parameter]})
            actual_gate = circ._get_whole_gates()

            expected_gate = \
                np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, 0, 1, 0],
                          [0, 0, 0, 0, 0, 0, 0, 1]]) * np.exp(1j*parameter)

            self.assertIsNone(
                np.testing.assert_allclose(actual_gate, expected_gate))

    def test_scalar_multi_target(self,):

        test_patterns = [
            (3, [0, 1], np.pi/3.),
            (3, [0, 1, 2], np.pi/5.),
            (3, [0, 2], np.pi/7.)
        ]

        for num_qubit, target_qubit, parameter in test_patterns:

            circ = StateVectorCircuit(num_qubit)
            circ.add_gate(
                {"name": "scalar",
                    "target_qubit": target_qubit,
                    "control_qubit": [],
                    "control_value": [],
                    "parameter": [parameter]})
            actual_gate = circ._get_whole_gates()

            expected_gate = \
                np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                          [0, 1, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 1, 0, 0, 0, 0],
                          [0, 0, 0, 0, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 1, 0, 0],
                          [0, 0, 0, 0, 0, 0, 1, 0],
                          [0, 0, 0, 0, 0, 0, 0, 1]]) \
                * np.exp(1j*parameter*len(target_qubit))

            self.assertIsNone(
                np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_swap(self,):
        circ = StateVectorCircuit(2)
        circ.add_gate(
            {"name": "swap", "target_qubit": [0, 1], "control_qubit": [],
             "control_value": [], "parameter": []})
        actual_gate = circ._get_whole_gates()

        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 0, 1]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_cswap(self,):
        circ = StateVectorCircuit(3)
        circ.add_gate(
            {"name": "swap", "target_qubit": [1, 2], "control_qubit": [0],
             "control_value": [1], "parameter": []})
        actual_gate = circ._get_whole_gates()
        expected_gate = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 1, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 1, 0],
                                  [0, 0, 0, 0, 0, 1, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 1]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_iswap(self,):
        circ = StateVectorCircuit(2)
        circ.add_gate(
            {"name": "iswap", "target_qubit": [0, 1], "control_qubit": [],
             "control_value": [], "parameter": []})
        actual_gate = circ._get_whole_gates()
        expected_gate = np.array([[1, 0, 0, 0],
                                  [0, 0, 1j, 0],
                                  [0, 1j, 0, 0],
                                  [0, 0, 0, 1]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate,
                                       atol=1e-16))

    def test_get_whole_gates_ccswap(self,):
        circ = StateVectorCircuit(4)
        circ.add_gate(
            {"name": "swap", "target_qubit": [2, 3], "control_qubit": [0, 1],
             "control_value": [1, 1], "parameter": []})
        actual_gate = circ._get_whole_gates()
        expected_gate = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        ])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_get_whole_gates_ciswap(self,):
        circ = StateVectorCircuit(3)
        circ.add_gate(
            {"name": "iswap", "target_qubit": [1, 2], "control_qubit": [0],
             "control_value": [1], "parameter": []})
        actual_gate = circ._get_whole_gates()
        expected_gate = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                                  [0, 1, 0, 0, 0, 0, 0, 0],
                                  [0, 0, 1, 0, 0, 0, 0, 0],
                                  [0, 0, 0, 1, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 1, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 1j, 0],
                                  [0, 0, 0, 0, 0, 1j, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 1]])
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate,
                                       atol=1e-16))
