import unittest

from quri_parts.circuit import QuantumCircuit

from .state_vector_assertion import assert_state_vector_matches


class TestStateVectorCircuitNonParametricTwoQubitGate(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest \
        test.with_quri_parts_and_qulacs.simulator.state_vector_circuit.test_non_parametric_single_qubit_gate
    ..
    ----------------------------------------------------------------------
    Ran 2 tests in 0.006s

    OK
    $
    """
    def test_swap_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_SWAP_gate(0, 1)
        assert_state_vector_matches(qc, self)

    def test_cz_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_CZ_gate(0, 1)
        assert_state_vector_matches(qc, self)

    def test_cnot_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_CZ_gate(0, 1)
        assert_state_vector_matches(qc, self)
