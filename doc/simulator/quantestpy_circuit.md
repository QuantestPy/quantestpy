# quantestpy.QuantestPyCircuit

## CLASS QuantestPyCircuit(num_qubit)

Creates a new circuit.

Currently the assert methods accept only `quantestpy.QuantestPyCircuit`, `qiskit.QuantumCircuit` and `OpenQASM 2.0 string` as circuits. For those who use their own circuit class, it is suggested to write a converter from it to `quantestpy.QuantestPyCircuit`. This can be done easily by using the [add_gate](./quantestpy_circuit_add_gate.md) method. The [converter](../../quantestpy/converter/sdk/qiskit.py) from `qiskit.QuantumCircuit` to `quantestpy.TestCircuit` is a good reference for this.

### Parameters
#### num_qubit : int
The number of qubits in the circuit.

### Methods

#### [add_gate](./quantestpy_circuit_add_gate.md)
Adds a gate in the circuit.

#### [draw](./quantestpy_circuit_draw.md)
Draws the circuit.

### Attributes

#### gates : list
Returns a list of gates in the order that the gates were added.

#### num_qubit : int
Returns the number of qubits.

#### qubit_indices : list
Returns a list of qubit indices starting from 0, i.e. [0, 1, ..., num_qubit-1].

### Examples
Create a new circuit instance with 5 qubits:
```py
qc = qp.QuantestPyCircuit(5)
```
