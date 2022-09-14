# QuantestPy
QuantestPy is an unit testing framework for quantum computing programs.


# Installation
We encourage installing QuantestPy via the pip tool(a python package manager).
The folllowing command installs the core QuantestPy component.
```bash
pip install git+https://github.com/QuantestPy/quantestpy.git
```


# Testing approaches with QuantestPy
You insert assert methods in your source codes.
```py
# your_source_code.py
import quantestpy as qp

state_vec = [0.7072+0j, 0, 0, 0.7072+0j]

# check that the state vector is normalized.
qp.state_vector.assert_is_normalized(state_vector_subject_to_test=state_vec)

...
```

QuantestPy provides several assert methods to check for and report failures. The following table lists the available methods:

Method | Checks that
--- | ---
[state_vector.assert_is_normalized(state_vec)](./doc/state_vector_assert_is_normalized.md) | `state_vec is normalized`
state_vector.assert_equal(state_vec_a, state_vec_b) | `state_vec_a == state_vec_b`
operator.assert_is_unitary(operator) | `operator is unitary`
operator.assert_equal(operator_a, operator_b) | `operator_a == operator_b`
circuit.assert_equal_to_operator(circuit, operator) | `circuit == operator`
circuit.assert_is_zero(circuit, qubits) | `qubits in circuit are |0>`
circuit.assert_ancilla_is_zero(circuit, ancilla_qubits) | `ancilla_qubits in circuit are always |0>`
circuit.assert_equal(circuit_a, circuit_b) | `circuit_a == circuit_b`

All the assert methods accept a msg argument that, if specified, is added to the error message on failure. The hyperlinks bring you to details of the methods.

# License
[Apache License 2.0](LICENSE.txt)


## how to create a quantum circuit
A quantum circuit is created via TestCircuit.
You can use qiskit or OpenQASM 2.0, which are converted into TestCircuit in QuantestPy.
```Py
from quantestpy import TestCircuit
circ = TestCircuit(3) #3qubits
circ.add_gate(
            {"name": "cx",
                "target_qubit": [1, 2],
                "control_qubit": [0],
                "control_value": [1],
                "parameter": []}
)
```
## Tests for state vectors
### Normalization of a vector
```Py
import numpy as np
from quantestpy import state_vector
state_vector_subject_to_test = [1,1,0,0]
state_vector.assert_is_normalized(state_vector_subject_to_test)
# The error message is below:
# quantestpy.exceptions.QuantestPyAssertionError: The state vector is not normalized.
# Norm: 1.41421
```
### Equivalence of vectors
```Py
import numpy as np
from quantestpy import state_vector
a = np.array([1,0,0,0])
b = np.array([0,1,0,0])
state_vector.assert_equal(a, b)
# The error message is below:
# quantestpy.exceptions.QuantestPyAssertionError:
# 0th element:
# a: 1
# b: 0
#
# 1th element:
# a: 0
# b: 1
```
## Tests for matrices
### Unitarity of a matrix
```Py
import numpy as np
from quantestpy import operator
operator_subject_to_test = np.array([[1,1],[1,1]])
operator.assert_is_unitary(operator_subject_to_test)
# The error message is below:
# quantestpy.exceptions.QuantestPyAssertionError: Operator is not unitary.
# m * m^+:
# [[2 2]
#  [2 2]]
```
### Equivalence of matrices
```Py
import numpy as np
from quantestpy import operator
a = np.array([[1,1],[1,1]])
b = np.array([[0,1],[1,1]])
operator.assert_equal(a, b)
# The error message is below:
# quantestpy.exceptions.QuantestPyAssertionError:
# 0th element:
# a: 1
# b: 0
```
## Tests for circuits
### Equivalence of circuits
```Py
from qiskit import QuantumCircuit
from quantestpy import circuit

"""
q_0: ──■──
       │
q_1: ──■──
     ┌─┴─┐
q_2: ┤ X ├
     └───┘
"""
qc_0 = QuantumCircuit(3)
qc_0.ccx(0, 1, 2)

"""

                                                                  ┌───┐
q_0: ───────────────────■─────────────────────■────■───────────■──┤ T ├
                        │            ┌─────┐  │  ┌─┴─┐┌─────┐┌─┴─┐├───┤
q_1: ───────■───────────┼─────────■──┤ Tdg ├──┼──┤ X ├┤ Tdg ├┤ X ├┤ S ├
     ┌───┐┌─┴─┐┌─────┐┌─┴─┐┌───┐┌─┴─┐├─────┤┌─┴─┐├───┤└┬───┬┘└───┘└───┘
q_2: ┤ H ├┤ X ├┤ Tdg ├┤ X ├┤ T ├┤ X ├┤ Tdg ├┤ X ├┤ T ├─┤ H ├───────────
     └───┘└───┘└─────┘└───┘└───┘└───┘└─────┘└───┘└───┘ └───┘

"""
qc_1 = QuantumCircuit(3)
qc_1.h(2)
qc_1.cx(1, 2)
qc_1.tdg(2)
qc_1.cx(0, 2)
qc_1.t(2)
qc_1.cx(1, 2)
qc_1.tdg(2)
qc_1.cx(0, 2)
qc_1.tdg(1)
qc_1.t(2)
qc_1.cx(0, 1)
qc_1.h(2)
qc_1.tdg(1)
qc_1.cx(0, 1)
qc_1.t(0)
qc_1.s(1)

circuit.assert_equal(
    qiskit_circuit_a=qc_0,
    qiskit_circuit_b=qc_1,
    number_of_decimal_places=15
)

```
### Correspandence of a circuit to a unitary matrix
```Py
import numpy as np
from quantestpy import TestCircuit
from quantestpy import circuit
# Prepare the Bell state
test_circ = TestCircuit(2)
test_circ.add_gate(
    {"name": "h", "target_qubit": [0], "control_qubit": [],
        "control_value": [], "parameter": []})
test_circ.add_gate(
    {"name": "cx", "control_qubit": [0],  "target_qubit": [1],
        "control_value": [1], "parameter": []})
expected_operator = np.array(
            [[1, 0, 1, 0],
             [0, 1, 0, 1],
             [0, 1, 0, -1],
             [1, 0, -1, 0]]
        )/np.sqrt(2.)
circuit.assert_equal_to_operator(operator_=expected_operator,
                                 test_circuit=test_circ)
```
### Appropriateness of ancilla qubits
```Py
from qiskit import QuantumCircuit
import qiskit
from quantestpy import circuit

"""
q_0: ──■───────────────────────────────────────■──
     ┌─┴─┐                                   ┌─┴─┐
q_1: ┤ X ├──■─────────────────────────────■──┤ X ├
     └───┘┌─┴─┐                         ┌─┴─┐└───┘
q_2: ─────┤ X ├──■───────────────────■──┤ X ├─────
          └───┘┌─┴─┐               ┌─┴─┐└───┘
q_3: ──────────┤ X ├──■─────────■──┤ X ├──────────
               └───┘┌─┴─┐     ┌─┴─┐└───┘
q_4: ───────────────┤ X ├──■──┤ X ├───────────────
                    └───┘┌─┴─┐└───┘
q_5: ────────────────────┤ X ├────────────────────
                         └───┘

q_0 and q_5 are system qubits while q_1 to q_4 are ancilla qubits.
"""
qc = QuantumCircuit(6)

# V
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
qc.cx(3, 4)
qc.cx(4, 5)

# Uncomputation; wrong order!
qc.cx(3, 4)
qc.cx(2, 3)
qc.cx(0, 1) # These two lines are reversed.
qc.cx(1, 2) # These two lines are reversed.

circuit.assert_ancilla_is_zero(
    qiskit_circuit=qc,
    ancilla_qubits=[1, 2, 3, 4]
)

# The error message is below:
# quantestpy.exceptions.QuantestPyAssertionError: qubit(s) [2] are either non-zero or entangled with other qubits.
```

