import unittest

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.simulator.state_vector_circuit import \
    cvt_quantestpy_circuit_to_state_vector_circuit


class TestStateVectorCircuitIdGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.with_qiskit.simulator.state_vector_circuit.test_id_gate
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.005s

    OK
    $
    """

    def test_id(self,):
        qc = QuantumCircuit(3)
        qc.id(0)
        expected_gate = np.array(Operator(qc))

        qpc = cvt_input_circuit_to_quantestpy_circuit(qc)
        svc = cvt_quantestpy_circuit_to_state_vector_circuit(qpc)
        svc._from_right_to_left_for_qubit_ids = True
        actual_gate = svc._get_whole_gates()

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_i(self,):
        qc = QuantumCircuit(3)
        qc.i(0)
        expected_gate = np.array(Operator(qc))

        qpc = cvt_input_circuit_to_quantestpy_circuit(qc)
        svc = cvt_quantestpy_circuit_to_state_vector_circuit(qpc)
        svc._from_right_to_left_for_qubit_ids = True
        actual_gate = svc._get_whole_gates()

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))
