import unittest

import numpy as np
from qiskit import QuantumCircuit

from quantestpy import TestCircuit
from quantestpy.converter import (_cvt_openqasm_to_test_circuit,
                                  _cvt_qiskit_to_test_circuit)


class TestConverter(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_converter
    ...
    ----------------------------------------------------------------------
    Ran 5 tests in 0.041s

    OK
    """

    def test__cvt_qiskit_to_test_circuit(self,):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        actual_circuit = _cvt_qiskit_to_test_circuit(qc)

        expected_circuit = TestCircuit(2)
        expected_circuit.add_gate(
            {"name": "h", "target_qubit": [0], "control_qubit": [],
             "control_value": [], "parameter": []})
        expected_circuit.add_gate({"name": "cx", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})

        self.assertEqual(vars(actual_circuit), vars(expected_circuit))

    def test__cvt_openqasm_to_test_circuit(self,):
        qc = QuantumCircuit(2, 2)
        qc.h(0)
        qc.cx(0, 1)
        qasm = qc.qasm()
        actual_circuit = _cvt_openqasm_to_test_circuit(qasm)

        expected_circuit = TestCircuit(2)
        expected_circuit.add_gate(
            {"name": "h", "target_qubit": [0], "control_qubit": [],
             "control_value": [], "parameter": []})
        expected_circuit.add_gate({"name": "cx", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})

        self.assertEqual(vars(actual_circuit), vars(expected_circuit))

    def test__cvt_qiskit_to_test_circuit_control_gates_1(self,):
        qc = QuantumCircuit(3)
        qc.cx(0, 1)
        qc.cy(0, 1)
        qc.cz(0, 1)
        qc.ch(0, 1)
        actual_circuit = _cvt_qiskit_to_test_circuit(qc)

        expected_circuit = TestCircuit(3)
        expected_circuit.add_gate({"name": "cx", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})
        expected_circuit.add_gate({"name": "cy", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})
        expected_circuit.add_gate({"name": "cz", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})
        expected_circuit.add_gate({"name": "ch", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": []})
        self.assertEqual(vars(actual_circuit), vars(expected_circuit))

    def test__cvt_qiskit_to_test_circuit_control_gates_2(self,):
        theta = np.pi/4

        qc = QuantumCircuit(3)
        qc.crx(theta, 0, 1)
        qc.cry(theta, 0, 1)
        qc.crz(theta, 0, 1)
        actual_circuit = _cvt_qiskit_to_test_circuit(qc)

        expected_circuit = TestCircuit(3)
        expected_circuit.add_gate({"name": "crx", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta]})
        expected_circuit.add_gate({"name": "cry", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta]})
        expected_circuit.add_gate({"name": "crz", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta]})

        self.assertEqual(vars(actual_circuit), vars(expected_circuit))

    def test__cvt_qiskit_to_test_circuit_control_gates_3(self,):
        theta = np.pi/4
        phi = np.pi/8
        lambda_ = np.pi/16

        qc = QuantumCircuit(3)
        qc.cu1(theta, 0, 1)
        qc.cu3(theta, phi, lambda_, 0, 1)
        qc.ccx(0, 1, 2)
        actual_circuit = _cvt_qiskit_to_test_circuit(qc)

        expected_circuit = TestCircuit(3)
        expected_circuit.add_gate({"name": "cu1", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta]})
        expected_circuit.add_gate({"name": "cu3", "target_qubit": [1],
                                   "control_qubit": [0], "control_value": [1],
                                   "parameter": [theta, phi, lambda_]})
        expected_circuit.add_gate({"name": "cx", "target_qubit": [2],
                                   "control_qubit": [0, 1],
                                   "control_value": [1, 1],
                                   "parameter": []})

        self.assertEqual(vars(actual_circuit), vars(expected_circuit))

    def test__cvt_qiskit_to_test_circuit_global_phase(self,):

        qc = QuantumCircuit(3, global_phase=np.pi/7.)
        qc.h(0)
        qc.ccx(0, 1, 2)
        actual_circuit = _cvt_qiskit_to_test_circuit(qc)

        expected_circuit = TestCircuit(3)
        expected_circuit.add_gate({"name": "h",
                                   "target_qubit": [0],
                                   "control_qubit": [],
                                   "control_value": [],
                                   "parameter": []})
        expected_circuit.add_gate({"name": "cx",
                                   "target_qubit": [2],
                                   "control_qubit": [0, 1],
                                   "control_value": [1, 1],
                                   "parameter": []})
        expected_circuit.add_gate({"name": "scalar",
                                   "target_qubit": [0],
                                   "control_qubit": [],
                                   "control_value": [],
                                   "parameter": [np.pi/7.]})

        self.assertEqual(vars(actual_circuit), vars(expected_circuit))
