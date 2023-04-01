import unittest

import numpy as np
from qiskit import QuantumCircuit

from quantestpy import QuantestPyCircuit
from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.exceptions import QuantestPyError


class TestConverterToQuantestPyCircuit(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.with_qiskit.test_converter_to_quantestpy_circuit
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.101s

    OK
    """

    def test_cvt_quantestpy_circuit(self,):
        input_circuit = QuantestPyCircuit(10)
        qc = cvt_input_circuit_to_quantestpy_circuit(input_circuit)
        self.assertIsInstance(qc, QuantestPyCircuit)

    def test_cvt_qasm(self,):
        input_circuit = QuantumCircuit(3).qasm()
        qc = cvt_input_circuit_to_quantestpy_circuit(input_circuit)
        self.assertIsInstance(qc, QuantestPyCircuit)

    def test_cvt_qiskit(self,):
        input_circuit = QuantumCircuit(3)
        qc = cvt_input_circuit_to_quantestpy_circuit(input_circuit)
        self.assertIsInstance(qc, QuantestPyCircuit)

    def test_cvt_others(self,):
        input_circuit = np.array([0, 1])
        expected_error_msg = "Input circuit must be one of the following: " \
            + "qasm, qiskit.QuantumCircuit," \
            + "quri_parts.circuit.NonParametricQuantumCircuit," \
            + "quri_parts.circuit.ImmutableBoundParametricQuantumCircuit," \
            + "and QuantestPyCircuit."

        with self.assertRaises(QuantestPyError) as cm:
            _ = cvt_input_circuit_to_quantestpy_circuit(input_circuit)

        self.assertEqual(cm.exception.args[0], expected_error_msg)
