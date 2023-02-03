# quantestpy.assert_ancilla_reset

## assert_ancilla_reset(circuit, ancilla_qubits, atol=1e-8, msg=None)

Raises a QuantestPyAssertionError if ancilla qubits of the circuit are either not 0 or entangled with other qubits up to desired tolerance.

Internally [quantestpy.assert_qubit_reset_to_zero_state](./assert_qubit_reset_to_zero_state.md) is called repeatedly for all possible states of the non-ancilla qubit(s) in the computation basis.

### Parameters

#### circuit : \{quantestpy.QuantestPyCircuit, qiskit.QuantumCircuit, OpenQASM 2.0 string\}
The circuit to test. [quantestpy.QuantestPyCircuit](../simulator/quantestpy_circuit.md) is a circuit class developed in this project.

#### ancilla_qubits : list(int)
The qubit(s) desired to be 0.

#### atol : float, optional
Absolute tolerance.

#### msg : \{None, str\}, optional
The message to be added to the error message on failure.

### Examples

```py
>>>> qc = qiskit.QuantumCircuit(6)
...: qc.cx(0, 1)
...: qc.cx(1, 2)
...: qc.cx(2, 3)
...: qc.cx(3, 4)
...: qc.cx(4, 5)
>>>> qc.cx(3, 4)
...: qc.cx(2, 3)
...: qc.cx(1, 3)  # Uncomputation fails. qc.cx(1, 2) is correct.
...: qc.cx(0, 1)
>>>> qp.assert_ancilla_reset(qc, ancilla_qubits=[1, 2, 3, 4])
Traceback (most recent call last):
     ...
QuantestPyAssertionError: qubit(s) [2, 3] are either non-zero or entangled with other qubits.
```
