import unittest

import numpy as np

from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from quantestpy import StateVectorCircuit


class TestStateVectorCircuitCSwapGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.state_vector_circuit.test_iswap_gate
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.006s

    OK
    $
    """

    def test_iswap_control_value_1(self,):
        circ = StateVectorCircuit(3)
        circ.add_gate({"name": "iswap",
                       "target_qubit": [2, 1], "control_qubit": [],
                       "control_value": [], "parameter": []})

        actual_gate = circ._get_whole_gates()

        qc = QuantumCircuit(3)
        qc.iswap(0, 1)
        expected_gate = np.array(Operator(qc))

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))
