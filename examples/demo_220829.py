import numpy as np
from qiskit import QuantumCircuit

from quantestpy import TestCircuit, circuit


"""Demo 1"""

"""
q_0: ──■──
     ┌─┴─┐
q_1: ┤ X ├
     └───┘
"""
test_circuit = TestCircuit(num_qubit=2)
test_circuit.add_gate(
    {"name": "cx",
     "control_qubit": [0],
     "target_qubit": [1],
     "control_value": [1],
     "parameter": []
     }
)
test_circuit._get_whole_gates()

"""
q_0: ──O──
     ┌─┴─┐
q_1: ┤ X ├
     └───┘
"""
test_circuit = TestCircuit(num_qubit=2)
test_circuit.add_gate(
    {"name": "cx",
     "control_qubit": [0],
     "target_qubit": [1],
     "control_value": [0],
     "parameter": []
     }
)
test_circuit._get_whole_gates()

"""
q_0: ──■──
       │
q_1: ──■──
     ┌─┴─┐
q_2: ┤ X ├
     └───┘
"""
test_circuit = TestCircuit(num_qubit=3)
test_circuit.add_gate(
    {"name": "cx",
     "control_qubit": [0, 1],
     "target_qubit": [2],
     "control_value": [1, 1],
     "parameter": []
     }
)
test_circuit._get_whole_gates()

"""Demo 2"""

expected_operator = np.array(
    [[1, 0, 1, 0],
     [0, 1, 0, 1],
     [0, 1, 0, -1],
     [1, 0, -1, 0]]
)/np.sqrt(2.)

"""
Qiskit
"""
qiskit_circuit = QuantumCircuit(2)
qiskit_circuit.h(0)
qiskit_circuit.cx(0, 1)
qiskit_circuit.draw()

circuit.assert_equal_to_operator(
    operator_=expected_operator,
    qiskit_circuit=qiskit_circuit
)

"""
Qasm
"""
qasm = qiskit_circuit.qasm()
print(qasm)

circuit.assert_equal_to_operator(
    operator_=expected_operator,
    qasm=qasm
)

"""
Demo 3
"""
qc = QuantumCircuit(4)
# V
qc.cx(0, 1)
qc.cx(1, 2)

# uncomputation
qc.cx(1, 3)

# V^{-1}
qc.cx(1, 2)
qc.cx(0, 1)

qc.draw()

circuit.assert_ancilla_is_zero(
    qiskit_circuit=qc,
    ancilla_qubits=[1, 2]
)
"""How to obtain all the computational bases for two system qubits
1
|0> ---    |0> ---
|0> --- => |0> ---

2
|0> --[X}--    |1> ---
|0> ------- => |0> ---

3
|0> -------    |0> ---
|0> --[X]-- => |1> ---

4
|0> --[X]--    |1> ---
|0> --[X]-- => |1> ---
"""

"""
Demo 4
"""
"""Toffoli"""
qc = QuantumCircuit(3)
qc.ccx(0, 1, 2)

tc = TestCircuit(num_qubit=3)
tc.add_gate(
    {"name": "cx",
     "control_qubit": [0, 1],
     "target_qubit": [2],
     "control_value": [1, 1],
     "parameter": []
     }
)

circuit.assert_equal(
    qiskit_circuit_a=qc,
    test_circuit_b=tc
)

"""CNOT(1, 0)
     ┌───┐     ┌───┐
q_0: ┤ H ├──■──┤ H ├
     ├───┤┌─┴─┐├───┤
q_1: ┤ H ├┤ X ├┤ H ├
     └───┘└───┘└───┘
=
     ┌───┐
q_0: ┤ X ├
     └─┬─┘
q_1: ──■──
"""
qc = QuantumCircuit(2)
qc.h([0, 1])
qc.cx(0, 1)
qc.h([0, 1])

tc = TestCircuit(num_qubit=2)
tc.add_gate(
    {"name": "cx",
     "control_qubit": [1],
     "target_qubit": [0],
     "control_value": [1],
     "parameter": []
     }
)

circuit.assert_equal(
    qiskit_circuit_a=qc,
    test_circuit_b=tc
)

"""Matrix norm
"""
qc = QuantumCircuit(2)
qc.h([0, 1])
qasm = qc.qasm()

tc = TestCircuit(num_qubit=2)
tc.add_gate(
    {"name": "x",
     "control_qubit": [],
     "target_qubit": [0, 1],
     "control_value": [],
     "parameter": []
     }
)

circuit.assert_equal(
    qasm_a=qasm,
    test_circuit_b=tc,
    matrix_norm_type="operator_norm_1",
    tolerance_for_matrix_norm_value=0.5
)

circuit.assert_equal(
    qasm_a=qasm,
    test_circuit_b=tc,
    matrix_norm_type="operator_norm_2",
    tolerance_for_matrix_norm_value=0.5
)

circuit.assert_equal(
    qasm_a=qasm,
    test_circuit_b=tc,
    matrix_norm_type="operator_norm_inf",
    tolerance_for_matrix_norm_value=0.5
)

circuit.assert_equal(
    qasm_a=qasm,
    test_circuit_b=tc,
    matrix_norm_type="Frobenius_norm",
    tolerance_for_matrix_norm_value=0.5
)

circuit.assert_equal(
    qasm_a=qasm,
    test_circuit_b=tc,
    matrix_norm_type="max_norm",
    tolerance_for_matrix_norm_value=1.
)

circuit.assert_equal(
    qasm_a=qasm,
    test_circuit_b=tc,
    matrix_norm_type="max_norm"
)
