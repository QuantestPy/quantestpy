# quantestpy.PauliCircuit.set_qubit_value

## PauliCircuit.set_qubit_value(qubit_idx, qubit_val)
Sets the state(s) of qubit(s) either `|0>` or `|1>`.

The default is all the qubits being initialized to `|0>`.

### Parameters

#### qubit_idx : list(int)
qubit index(indices)

#### qubit_val : list(int)
qubit value(s), either 0 or 1. The length of `qubit_val` must be equal to that of `qubit_idx`.

### Examples
Set the states of only the qubits 0 and 1 in `|1>` while the others in `|0>`:
```py
0  |1> ─

1  |1> ─

2  |0> ─

3  |0> ─

4  |0> ─

pc = PauliCircuit(5)
pc.set_qubit_value([0, 1], [1, 1])
```
