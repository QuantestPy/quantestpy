import unittest

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info.operators import Operator

from quantestpy import StateVectorCircuit


class TestStateVectorCircuitSwapGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.simulator.state_vector_circuit.test_swap_gate
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.005s

    OK
    $
    """

    def test_cswap_control_value_1(self,):
        circ = StateVectorCircuit(3)
        circ.add_gate({"name": "swap",
                       "target_qubit": [0, 1], "control_qubit": [2],
                       "control_value": [1], "parameter": []})

        actual_gate = circ._get_whole_gates()

        qc = QuantumCircuit(3)
        qc.cswap(0, 1, 2)
        expected_gate = np.array(Operator(qc))

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_cswap_control_value_0(self,):
        circ = StateVectorCircuit(3)
        circ.add_gate({"name": "swap",
                       "target_qubit": [0, 1], "control_qubit": [2],
                       "control_value": [0], "parameter": []})

        actual_gate = circ._get_whole_gates()

        qc = QuantumCircuit(3)
        qc.cswap(0, 1, 2, None, "0")
        expected_gate = np.array(Operator(qc))

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))

    def test_fredkin(self,):
        circ = StateVectorCircuit(3)
        circ.add_gate({"name": "swap",
                       "target_qubit": [0, 1], "control_qubit": [2],
                       "control_value": [1], "parameter": []})

        actual_gate = circ._get_whole_gates()

        qc = QuantumCircuit(3)
        qc.fredkin(0, 1, 2)
        expected_gate = np.array(Operator(qc))

        self.assertIsNone(
            np.testing.assert_allclose(actual_gate, expected_gate))
