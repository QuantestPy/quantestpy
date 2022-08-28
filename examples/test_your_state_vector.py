"""
Example showing how to test a state vector
"""

import numpy as np
import qiskit
from qiskit.quantum_info import Statevector

from quantestpy import state_vector

# build my circuit
qc = qiskit.QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# here I want to test my state vector: v1
state_vector_from_qiskit = Statevector(qc)
state_vector_from_qiskit = np.array(state_vector_from_qiskit)

expected_state_vector = - np.array([1, 0, 0, 1]) / np.sqrt(2.)

state_vector.assert_equal(
    state_vector_from_qiskit,
    expected_state_vector,
    number_of_decimal_places=5,
    up_to_global_phase=True
)
