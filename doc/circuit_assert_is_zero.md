# quantestpy.circuit.assert_is_zero

## circuit.assert_is_zero(circuit, qubits=None, atol=1e-8, msg=None)

Raises a QuantestPyAssertionError if qubits of the circuit are either not 0 or entangled with other qubits up to desired tolerance.

The circuit `circuit` is converted to an operator and eventually to a state vector. The test verifies
```py
abs(selected elements of the state vector) <= atol
```
where `selected elements of the state vector` can be anticipated from `qubits`.

### Parameters

#### circuit: \{quantestpy.TestCircuit, qiskit.QuantumCircuit, OpenQASM 2.0 string\}
The circuit to test. [quantestpy.TestCircuit](./test_circuit.md) is a circuit class developed in this project.

#### qubits: \{None, list(int)\}, optional
The qubit(s) desired to be 0. If None, all qubits are chosen.

#### atol : float, optional
Absolute tolerance.

#### msg : \{None, str\}, optional
The message to be added to the error message on failure.

### Examples

```py
>>>> qc = qiskit.QuantumCircuit(3)
>>>> qc.x(2)  # qubit 2 is no longer 0
>>>> qp.circuit.assert_is_zero(qc, qubits=[0, 2])
Traceback (most recent call last):
     ...
QuantestPyAssertionError: qubit(s) [2] are either non-zero or entangled with other qubits.
```
