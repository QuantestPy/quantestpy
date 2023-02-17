import unittest

from quri_parts.circuit import QuantumCircuit
from simulator.state_vector_circuit.state_vector_assertion import \
    assert_state_vector_matches


class TestQuriPartsConverter(unittest.TestCase):
    """
    How to execute this test:
    $ pwd
    {Your directory where you git-cloned quantestpy}/quantestpy
    $ python -m unittest test.with_quri_parts_and_qulacs.test_converter
    .......
    ----------------------------------------------------------------------
    Ran 7 tests in 0.066s

    OK
    """

    def test__cvt_quri_parts_to_quantestpy_circuit(self,):
        n_qubits = 2
        angle = 0.25
        qc = QuantumCircuit(n_qubits)
        qc.add_H_gate(0)
        qc.add_CNOT_gate(0, 1)
        qc.add_CZ_gate(0, 1)
        qc.add_RX_gate(0, angle)
        qc.add_RY_gate(0, angle)
        qc.add_RZ_gate(0, angle)
        qc.add_S_gate(0)
        qc.add_Sdag_gate(0)
        qc.add_SqrtX_gate(0)
        qc.add_SqrtXdag_gate(0)
        qc.add_SWAP_gate(0, 1)
        qc.add_T_gate(0)
        qc.add_Tdag_gate(0)
        qc.add_U3_gate(0, angle, angle, angle)
        qc.add_X_gate(0)
        qc.add_Y_gate(0)
        qc.add_Z_gate(0)
        assert_state_vector_matches(qc, self)
