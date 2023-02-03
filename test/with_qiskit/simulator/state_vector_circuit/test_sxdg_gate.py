import unittest

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from quantestpy import StateVectorCircuit
from quantestpy.simulator.state_vector_circuit import _SXdg


class TestStateVectorCircuitSXdgGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.state_vector_circuit.test_sxdg_gate
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.004s

    OK
    $
    """

    def test_sxdg(self,):
        circ = StateVectorCircuit(3)
        actual_gate = circ._create_all_qubit_gate_from_original_qubit_gate(
            _SXdg, control_qubit=[], target_qubit=[2], control_value=[]
        )

        qc = QuantumCircuit(3)
        qc.sxdg(0)
        expected_gate = np.array(Operator(qc))

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))
