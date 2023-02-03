import unittest

import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from quantestpy import StateVectorCircuit
from quantestpy.simulator.state_vector_circuit import _S


class TestStateVectorCircuitSGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.state_vector_circuit.test_s_gate
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.005s

    OK
    $
    """

    def test_cs_control_value_1(self,):
        circ = StateVectorCircuit(3)
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _S, control_qubit=[2], target_qubit=[1], control_value=[1]
        )

        qc = QuantumCircuit(3)
        qc.cs(0, 1)
        expected_gate = np.array(Operator(qc))

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cs_control_value_0(self,):
        circ = StateVectorCircuit(3)
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _S, control_qubit=[2], target_qubit=[1], control_value=[0]
        )

        qc = QuantumCircuit(3)
        qc.cs(0, 1, None, "0")
        expected_gate = np.array(Operator(qc))

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))
