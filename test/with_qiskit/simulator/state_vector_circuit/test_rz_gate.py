import unittest

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.simulator.state_vector_circuit import \
    cvt_quantestpy_circuit_to_state_vector_circuit


class TestStateVectorCircuitRyGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.with_qiskit.simulator.state_vector_circuit.test_rz_gate
    ....
    ----------------------------------------------------------------------
    Ran 4 tests in 0.010s

    OK
    $
    """

    def test_crz_control_value_1(self,):
        qc = QuantumCircuit(3)
        qc.crz(np.pi/4, 0, 1)
        expected_gate = np.array(Operator(qc))

        qpc = cvt_input_circuit_to_quantestpy_circuit(qc)
        svc = cvt_quantestpy_circuit_to_state_vector_circuit(qpc)
        svc._from_right_to_left_for_qubit_ids = True
        actual_gate = svc._get_whole_gates()

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_crz_control_value_0(self,):
        qc = QuantumCircuit(3)
        qc.crz(np.pi/4, 0, 1, None, "0")
        expected_gate = np.array(Operator(qc))

        qpc = cvt_input_circuit_to_quantestpy_circuit(qc)
        svc = cvt_quantestpy_circuit_to_state_vector_circuit(qpc)
        svc._from_right_to_left_for_qubit_ids = True
        actual_gate = svc._get_whole_gates()

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_rz(self,):
        qc = QuantumCircuit(3)
        qc.rz(np.pi/4, 0)
        expected_gate = np.array(Operator(qc))

        qpc = cvt_input_circuit_to_quantestpy_circuit(qc)
        svc = cvt_quantestpy_circuit_to_state_vector_circuit(qpc)
        svc._from_right_to_left_for_qubit_ids = True
        actual_gate = svc._get_whole_gates()

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    # qiskit.mcrz is multi-controlled Z rotation up to a global phase,
    # which means that qiskit.mcrz coincides with multi-controlled p gate.
    # (Namely, qiskit.mcrz is same as qiskit.mcp.)
    def test_mcrz(self,):
        qc = QuantumCircuit(3)
        qc.mcrz(np.pi/4, [0, 1], 2)
        expected_gate = np.array(Operator(qc))

        qpc = cvt_input_circuit_to_quantestpy_circuit(qc)
        svc = cvt_quantestpy_circuit_to_state_vector_circuit(qpc)
        svc._from_right_to_left_for_qubit_ids = True
        actual_gate = svc._get_whole_gates()

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))
