import unittest

import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from quantestpy import StateVectorCircuit
from quantestpy.simulator.state_vector_circuit import _ID


class TestStateVectorCircuitIdGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.state_vector_circuit.test_id_gate
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.005s

    OK
    $
    """

    def test_id(self,):
        circ = StateVectorCircuit(3)
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _ID, control_qubit=[], target_qubit=[2], control_value=[]
        )

        qc = QuantumCircuit(3)
        qc.id(0)
        expected_gate = np.array(Operator(qc))

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_i(self,):
        circ = StateVectorCircuit(3)
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _ID, control_qubit=[], target_qubit=[2], control_value=[]
        )

        qc = QuantumCircuit(3)
        qc.i(0)
        expected_gate = np.array(Operator(qc))

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))
