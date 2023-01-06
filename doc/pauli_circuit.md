# quantestpy.PauliCircuit

## CLASS PauliCircuit(num_qubit)

Creates a new circuit. In this circuit class a qubit is in a state either `|0>` or `|1>` with a global phase like a classical bit (i.e. no superpositions of these states) by limiting the gate operations to the Pauli and swap operations.

Currently some of the assert methods accept only this circuit class as input circuits. For those who use their own circuit class, it is suggested to write a converter from it to `quantestpy.PauliCircuit`. This can be done easily by using the [add_gate](./pauli_circuit_add_gate.md) method.


### Parameters
#### num_qubit : int
The number of qubits in the circuit.

### Methods

#### [add_gate](./pauli_circuit_add_gate.md)
Adds a gate in the circuit.

#### [set_qubit_value](./pauli_circuit_set_qubit_value.md)
Sets the state(s) of qubit(s) either `|0>` or `|1>`.

#### [draw](./pauli_circuit_draw.md)
Draws the circuit.

### Attributes
None.

### Examples
Create a new circuit object with 100 qubits:
```py
import quantestpy as qp
pc = qp.PauliCircuit(100)
```
