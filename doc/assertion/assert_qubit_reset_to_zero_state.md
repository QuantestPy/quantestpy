# quantestpy.assert_qubit_reset_to_zero_state

## assert_qubit_reset_to_zero_state(circuit, qubits=None, atol=1e-8, msg=None)

Raises a QuantestPyAssertionError if qubits of the circuit are either not 0 or entangled with other qubits up to desired tolerance.

The argument `circuit` is converted to an operator, which changes the initial state vector into the resulting state vector. When a user expects certain qubits specified by `qubits` to be 0 and not to be entangled with other qubit(s), corresponding element(s) of the obtained state vector should be 0. This is verified by the assert method, namely
```py
abs(corresponding element(s) of the final state_vector) <= atol
```

### Parameters

#### circuit : \{quantestpy.QuantestPyCircuit, qiskit.QuantumCircuit, OpenQASM 2.0 string\}
The circuit to test. [quantestpy.QuantestPyCircuit](../simulator/quantestpy_circuit.md) is a circuit class developed in this project.

#### qubits : \{None, list(int)\}, optional
The qubit(s) desired to be 0. If None, all qubits are chosen.

#### atol : float, optional
Absolute tolerance.

#### msg : \{None, str\}, optional
The message to be added to the error message on failure.

### Examples

```py
>>>> qc = qiskit.QuantumCircuit(3)
>>>> qc.x(2)  # qubit 2 is no longer 0
>>>> qp.assert_qubit_reset_to_zero_state(qc, qubits=[0, 2])
Traceback (most recent call last):
     ...
QuantestPyAssertionError: qubit(s) [2] are either non-zero or entangled with other qubits.
```
