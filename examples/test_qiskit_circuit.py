"""
Example showing how to test a qiskit circuit class that you build.
"""

import numpy as np
import qiskit

from quantestpy import circuit

# build my circuit
qc = qiskit.QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# here I want to test my circuit
qasm = qc.qasm()
expected_operator = np.array(
    [[1, 0, 1, 0],
     [0, 1, 0, 1],
     [0, 1, 0, -1],
     [1, 0, -1, 0]]
)/np.sqrt(2.) * np.exp(0.4j)

circuit.assert_equal_to_operator(
    expected_operator,
    qasm=qasm,
    up_to_global_phase=True
)
