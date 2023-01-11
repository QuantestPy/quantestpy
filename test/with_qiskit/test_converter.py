import unittest

import numpy as np
from qiskit import QuantumCircuit

from quantestpy import QuantestPyCircuit
from quantestpy.converter.sdk.qasm import _cvt_openqasm_to_quantestpy_circuit
from quantestpy.converter.sdk.qiskit import _cvt_qiskit_to_quantestpy_circuit
from quantestpy.simulator.state_vector_circuit import \
    cvt_quantestpy_circuit_to_state_vector_circuit


class TestConverter(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.with_qiskit.test_converter
    .......
    ----------------------------------------------------------------------
    Ran 7 tests in 0.066s

    OK
    """

    def test__cvt_qiskit_to_quantestpy_circuit(self,):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        actual_circuit = _cvt_qiskit_to_quantestpy_circuit(qc)

        expected_circuit = QuantestPyCircuit(2)
        expected_circuit.add_gate(
            {"name": "h", "target_qubit": [0], "control_qubit": [],
             "control_value": [], "parameter": []})
        expected_circuit.add_gate({"name": "x", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})

        actual_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            actual_circuit)._get_whole_gates()
        expected_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            expected_circuit)._get_whole_gates()
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test__cvt_openqasm_to_quantestpy_circuit(self,):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qasm = qc.qasm()
        actual_circuit = _cvt_openqasm_to_quantestpy_circuit(qasm)

        expected_circuit = QuantestPyCircuit(2)
        expected_circuit.add_gate(
            {"name": "h", "target_qubit": [0], "control_qubit": [],
             "control_value": [], "parameter": []})
        expected_circuit.add_gate({"name": "x", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})

        actual_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            actual_circuit)._get_whole_gates()
        expected_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            expected_circuit)._get_whole_gates()
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test__cvt_qiskit_to_quantestpy_circuit_control_gates_1(self,):
        qc = QuantumCircuit(3)
        qc.cx(0, 1)
        qc.cy(0, 1)
        qc.cz(0, 1)
        qc.ch(0, 1)
        actual_circuit = _cvt_qiskit_to_quantestpy_circuit(qc)

        expected_circuit = QuantestPyCircuit(3)
        expected_circuit.add_gate({"name": "x", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})
        expected_circuit.add_gate({"name": "y", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})
        expected_circuit.add_gate({"name": "z", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})
        expected_circuit.add_gate({"name": "h", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})

        actual_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            actual_circuit)._get_whole_gates()
        expected_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            expected_circuit)._get_whole_gates()
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate, atol=1e-15))

    def test__cvt_qiskit_to_quantestpy_circuit_control_gates_2(self,):
        theta = np.pi/4

        qc = QuantumCircuit(3)
        qc.crx(theta, 0, 1)
        qc.cry(theta, 0, 1)
        qc.crz(theta, 0, 1)
        actual_circuit = _cvt_qiskit_to_quantestpy_circuit(qc)

        expected_circuit = QuantestPyCircuit(3)
        expected_circuit.add_gate({"name": "rx", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta]})
        expected_circuit.add_gate({"name": "ry", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta]})
        expected_circuit.add_gate({"name": "rz", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta]})

        actual_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            actual_circuit)._get_whole_gates()
        expected_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            expected_circuit)._get_whole_gates()
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate, atol=1e-15))

    def test__cvt_qiskit_to_quantestpy_circuit_control_gates_3(self,):
        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16
        gamma = 0

        qc = QuantumCircuit(3)
        qc.cp(theta, 0, 1)
        qc.cu(theta, phi, lambda_, gamma, 0, 1)
        qc.ccx(0, 1, 2)
        actual_circuit = _cvt_qiskit_to_quantestpy_circuit(qc)

        expected_circuit = QuantestPyCircuit(3)
        expected_circuit.add_gate({"name": "p", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta]})
        expected_circuit.add_gate({"name": "u", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta, phi, lambda_, gamma]})
        expected_circuit.add_gate({"name": "x", "target_qubit": [2],
                                   "control_qubit": [0, 1],
                                   "control_value": [1, 1],
                                   "parameter": []})

        actual_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            actual_circuit)._get_whole_gates()
        expected_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            expected_circuit)._get_whole_gates()
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate, atol=1e-15))

    def test__cvt_qiskit_to_quantestpy_circuit_global_phase(self,):

        qc = QuantumCircuit(3, global_phase=np.pi/7.)
        qc.h(0)
        qc.ccx(0, 1, 2)
        actual_circuit = _cvt_qiskit_to_quantestpy_circuit(qc)

        expected_circuit = QuantestPyCircuit(3)
        expected_circuit.add_gate({"name": "h",
                                   "target_qubit": [0],
                                   "control_qubit": [],
                                   "control_value": [],
                                   "parameter": []})
        expected_circuit.add_gate({"name": "x",
                                   "target_qubit": [2],
                                   "control_qubit": [0, 1],
                                   "control_value": [1, 1],
                                   "parameter": []})
        expected_circuit.add_gate({"name": "scalar",
                                   "target_qubit": [0],
                                   "control_qubit": [],
                                   "control_value": [],
                                   "parameter": [np.pi/7.]})

        actual_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            actual_circuit)._get_whole_gates()
        expected_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            expected_circuit)._get_whole_gates()
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate, atol=1e-15))

    def test__cvt_qiskit_to_quantestpy_circuit_control_gates_4(self,):
        theta = np.pi/4
        phi = np.pi/8

        qc = QuantumCircuit(3)
        qc.r(theta, phi, 1)
        qc.crx(theta, 0, 1)
        qc.rx(theta, 2)
        qc.cry(theta, 0, 1)
        qc.ry(theta, 2)
        qc.crz(theta, 0, 1)
        qc.rz(theta, 2)

        actual_circuit = _cvt_qiskit_to_quantestpy_circuit(qc)

        expected_circuit = QuantestPyCircuit(3)
        expected_circuit.add_gate({"name": "r", "target_qubit": [1],
                                   "control_qubit": [], "control_value": [],
                                   "parameter": [theta, phi]})
        expected_circuit.add_gate({"name": "rx", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta]})
        expected_circuit.add_gate({"name": "rx", "target_qubit": [2],
                                   "control_qubit": [], "control_value": [],
                                   "parameter": [theta]})
        expected_circuit.add_gate({"name": "ry", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta]})
        expected_circuit.add_gate({"name": "ry", "target_qubit": [2],
                                   "control_qubit": [], "control_value": [],
                                   "parameter": [theta]})
        expected_circuit.add_gate({"name": "rz", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta]})
        expected_circuit.add_gate({"name": "rz", "target_qubit": [2],
                                   "control_qubit": [], "control_value": [],
                                   "parameter": [theta]})

        actual_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            actual_circuit)._get_whole_gates()
        expected_gate = cvt_quantestpy_circuit_to_state_vector_circuit(
            expected_circuit)._get_whole_gates()
        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate, atol=1e-15))
