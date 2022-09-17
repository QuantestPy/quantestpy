# quantestpy.TestCircuit

## CLASS TestCircuit(num_qubit)

Creates a new circuit.

Currently the assert methods accept only quantestpy.TestCircuit, qiskit.QuantumCircuit and OpenQASM 2.0 string as circuits. For those who do not have qiskit.QuantumCircuit or OpenQASM 2.0 string at hand, it is suggested to convert their circuit objects to quantestpy.TestCircuit objects. This can be done easily by using the [add_gate](./test_circuit_add_gate.md) method. The [converter](../quantestpy/converter.py) from `QasmQobj` to quantestpy.TestCircuit is a good reference for doing this systematically.

### Parameters
#### num_qubit : int
The number of qubits in the circuit.

### Methods

#### [add_gate](./test_circuit_add_gate.md)
Adds a gate in the circuit.

#### [set_initial_state_vector](./test_circuit_set_initial_state_vector.md)
Sets an arbitrary vector as the initial state of the circuit.

### Attributes
None.

### Examples
Create a new circuit object with 5 qubits:
```py
ts = qp.TestCircuit(5)
```

