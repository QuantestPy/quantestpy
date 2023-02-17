import unittest

from quri_parts.circuit import Identity, QuantumCircuit

from .state_vector_assertion import assert_state_vector_matches


class TestStateVectorCircuitNonParametricSingleQubitGate(unittest.TestCase):
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

    def test_h_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        assert_state_vector_matches(qc, self)

    def test_x_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_X_gate(0)
        assert_state_vector_matches(qc, self)

    def test_y_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_Y_gate(0)
        assert_state_vector_matches(qc, self)

    def test_z_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_Z_gate(0)
        assert_state_vector_matches(qc, self)

    def test_id_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_gate(Identity(0))
        assert_state_vector_matches(qc, self)

    def test_s_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_S_gate(0)
        assert_state_vector_matches(qc, self)

    def test_sdag_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_Sdag_gate(0)
        assert_state_vector_matches(qc, self)

    def test_sx_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_SqrtX_gate(0)
        assert_state_vector_matches(qc, self)

    def test_sxdag_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_SqrtXdag_gate(0)
        assert_state_vector_matches(qc, self)

    def test_t_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_T_gate(0)
        assert_state_vector_matches(qc, self)

    def test_tdag_gate(self,):
        n_qubits = 3
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_Tdag_gate(0)
        assert_state_vector_matches(qc, self)

    def test_rx_gate(self,):
        n_qubits = 3
        angle = 0.5
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_RX_gate(0, angle)
        assert_state_vector_matches(qc, self)

    def test_ry_gate(self,):
        n_qubits = 3
        angle = 0.5
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_RY_gate(0, angle)
        assert_state_vector_matches(qc, self)

    def test_rz_gate(self,):
        n_qubits = 3
        angle = 0.5
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_RZ_gate(0, angle)
        assert_state_vector_matches(qc, self)

    def test_u3_gate(self,):
        n_qubits = 3
        angle = [0.5, 0.25, 0.125]
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_U3_gate(0, angle[0], angle[1], angle[2])
        assert_state_vector_matches(qc, self)
