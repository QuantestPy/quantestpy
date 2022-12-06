# quantestpy.PauliCircuit.add_gate

## PauliCircuit.add_gate(gate)
Adds a gate in the circuit.

### Parameters

#### gate : dict
The gate to be added. The following key-values must be included:

key | value | type of value
--- | --- | ---
"name" | gate's name | str
"target_qubit" | target qubit(s) | list(int)
"control_qubit" | control qubit(s) | list(int)
"control_value" | control value(s) | list({0, 1})

Users can always put multi-indices in "target_qubit", "control_qubit" and "control_value" for any gate as long as they are not out of range for the circuit size. An exception is "swap" gate, which restricts itself to two indices in "target_qubit". Controlled gates can be defined by specifying a gate name being performed on a single target qubit (such as "x") and giving a non-empty list to "control_qubit". By providing a non-empty list of 0 and 1 to "control_value", users can define the condition on the control qubit(s) for the gate to be applied on the target qubit(s). By definition, the length of "control_value" must be equal to that of "control_qubit".

The following table lists the available gates:

name | description | matrix representation
--- | --- | ---
"x" | X gate | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;0&&space;1&space;\\&space;1&space;&&space;0&space;\end{bmatrix}" />
"y" | Y gate | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;0&space;&&space;-i&space;\\&space;i&space;&&space;0&space;\end{bmatrix}" />
"z" | Z gate | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;1&space;&&space;0&space;\\&space;0&space;&&space;-1&space;\end{bmatrix}" />
"swap" | Swap gate | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;1&space;&&space;0&space;&&space;0&space;&&space;0&space;\\&space;0&space;&&space;0&space;&&space;1&space;&&space;0&space;\\&space;0&space;&&space;1&space;&&space;0&space;&&space;0&space;\\&space;0&space;&&space;0&space;&&space;0&space;&&space;1&space;\end{bmatrix}" />

### Examples
X gate:
```py
0  |0> ─[X]─

1  |0> ─────

pc = PauliCircuit(2)
pc.add_gate({
    "name": "x",
    "target_qubit": [0],
    "control_qubit": [],
    "control_value": []
})
```
Toffoli gate, conditional on the control qubits being set to 1:
```py
0  |0> ──■──
         │
1  |0> ──■──
         │
2  |0> ─[X]─

pc = PauliCircuit(3)
pc.add_gate({
    "name": "x",
    "target_qubit": [2],
    "control_qubit": [0, 1],
    "control_value": [1, 1]
})
```
CZ gate, conditional on the control qubit being set to 0:
```py
0  |0> ──o──
         │
1  |0> ─[Z]─

pc = PauliCircuit(2)
pc.add_gate({
    "name": "z",
    "target_qubit": [1],
    "control_qubit": [0],
    "control_value": [0]
})
```
YY gate:
```py
0  |0> ─[Y]─

1  |0> ─[Y]─

pc = PauliCircuit(2)
pc.add_gate({
    "name": "y",
    "target_qubit": [0, 1],
    "control_qubit": [],
    "control_value": []
})
```
