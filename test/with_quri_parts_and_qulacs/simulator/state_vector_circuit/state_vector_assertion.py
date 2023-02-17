import unittest

import numpy as np
from qulacs import QuantumState
from quri_parts.circuit import QuantumCircuit
from quri_parts.qulacs.circuit import convert_circuit

from quantestpy.converter.converter_to_quantestpy_circuit import \
    cvt_input_circuit_to_quantestpy_circuit
from quantestpy.simulator.state_vector_circuit import \
    cvt_quantestpy_circuit_to_state_vector_circuit


def assert_state_vector_matches(circuit: QuantumCircuit,
                                test_instance: unittest.TestCase) -> None:
    n_qubits = circuit.qubit_count

    qpc = cvt_input_circuit_to_quantestpy_circuit(circuit)
    svc = cvt_quantestpy_circuit_to_state_vector_circuit(qpc)
    svc._from_right_to_left_for_qubit_ids = True
    quantestpy_state = svc. _get_state_vector()

    qulacs_circuit = convert_circuit(circuit)
    state = QuantumState(n_qubits)
    qulacs_circuit.update_quantum_state(state)

    test_instance.assertIsNone(
        np.testing.assert_allclose(quantestpy_state, state.get_vector()))
