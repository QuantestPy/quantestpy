import unittest
from qiskit import QuantumCircuit

from quantestpy import TestCircuit
from quantestpy.converter import _cvt_qiskit_to_test_circuit
from quantestpy.converter import _cvt_openqasm_to_test_circuit


class TestConverter(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.test_converter
    ...
    ----------------------------------------------------------------------
    Ran 2 tests in 0.035s

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
