# quantestpy.QuantestPyCircuit.add_gate

## QuantestPyCircuit.add_gate(gate)
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
"parameter" | parameter(s) | list(float)

Users can always put multi-indices in "target_qubit", "control_qubit" and "control_value" for any gate as long as they are not out of range for the circuit size. Exceptions are "swap" and "iswap" gates, which restrict themselves to two indices in "target_qubit". Controlled gates can be defined by specifying a gate name being performed on a single target qubit (such as "x") and giving a non-empty list to "control_qubit". By providing a non-empty list of 0 and 1 to "control_value", users can define the condition on the control qubit(s) for the gate to be applied on the target qubit(s). By definition, the length of "control_value" must be equal to that of "control_qubit". A non-empty list for "parameter" is allowed only for gates which have parameters such as rotation gates. For better understanding, see examples below.

The following table lists the currently available gates:

name | description | parameter | matrix representation
--- | --- | --- | ---
"id" | Identity gate | [] | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;1&space;&&space;0&space;\\&space;0&space;&&space;1&space;\end{bmatrix}" />
"x" | X gate | [] | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;0&&space;1&space;\\&space;1&space;&&space;0&space;\end{bmatrix}" />
"y" | Y gate | [] | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;0&space;&&space;-i&space;\\&space;i&space;&&space;0&space;\end{bmatrix}" />
"z" | Z gate | [] | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;1&space;&&space;0&space;\\&space;0&space;&&space;-1&space;\end{bmatrix}" />
"h" | Hadamard gate | [] | <img src="https://latex.codecogs.com/svg.image?\frac{1}{\sqrt{2}}\begin{bmatrix}&space;1&space;&&space;1&space;\\&space;1&space;&&space;-1&space;\end{bmatrix}" />
"s" | S gate | [] | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;1&space;&&space;0&space;\\&space;0&space;&&space;i&space;\end{bmatrix}" />
"sdg" | Hermitian conjugate of Phase gate | [] | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;1&space;&&space;0&space;\\&space;0&space;&&space;-i&space;\end{bmatrix}" />
"t" | T gate | [] | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;1&space;&&space;0&space;\\&space;0&space;&&space;e^{i\pi/4}&space;\end{bmatrix}" />
"tdg" | Hermitian conjugate of T gate | [] | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;1&space;&&space;0&space;\\&space;0&space;&&space;e^{-i\pi/4}&space;\end{bmatrix}" />
"swap" | Swap gate | [] | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;1&space;&&space;0&space;&&space;0&space;&&space;0&space;\\&space;0&space;&&space;0&space;&&space;1&space;&&space;0&space;\\&space;0&space;&&space;1&space;&&space;0&space;&&space;0&space;\\&space;0&space;&&space;0&space;&&space;0&space;&&space;1&space;\end{bmatrix}" />
"iswap" | iSwap gate | [] | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;1&space;&&space;0&space;&&space;0&space;&&space;0&space;\\&space;0&space;&&space;0&space;&&space;i&space;&&space;0&space;\\&space;0&space;&&space;i&space;&&space;0&space;&&space;0&space;\\&space;0&space;&&space;0&space;&&space;0&space;&&space;1&space;\end{bmatrix}" />
"rx" | Rx gate | $[\theta]$ | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;\cos{\frac{\theta}{2}}&space;&&space;-i\sin{\frac{\theta}{2}}&space;\\&space;-i\sin{\frac{\theta}{2}}&space;&&space;\cos{\frac{\theta}{2}}&space;\end{bmatrix}" />
"ry" | Ry gate | $[\theta]$ | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;\cos{\frac{\theta}{2}}&space;&&space;-\sin{\frac{\theta}{2}}&space;\\&space;\sin{\frac{\theta}{2}}&space;&&space;\cos{\frac{\theta}{2}}&space;\end{bmatrix}" />
"rz" | Rz gate | $[\phi]$ | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;e^{-i\phi/2}&space;&&space;0&space;\\&space;0&space;&&space;e^{i\phi/2}&space;\end{bmatrix}" />
"p" | Phase gate | $[\lambda]$ | <img src="https://latex.codecogs.com/svg.image?\begin{bmatrix}&space;1&space;&&space;0&space;\\&space;0&space;&&space;e^{i\lambda}&space;\end{bmatrix}" />
"u" | U gate | $[\theta, \phi, \lambda, \gamma]$ | <img src="https://latex.codecogs.com/svg.image?e^{i\gamma}\begin{bmatrix}&space;\cos{\frac{\theta}{2}}&space;&&space;-e^{i\lambda}\sin{\frac{\theta}{2}}&space;\\&space;e^{i\phi}\sin{\frac{\theta}{2}}&space;&&space;e^{i(\phi&plus;\lambda)}\cos{\frac{\theta}{2}}&space;\end{bmatrix}" />
"scalar" | $\exp{(i\theta)}$ * Identity gate | $[\theta]$ | <img src="https://latex.codecogs.com/svg.image?e^{i\theta}\begin{bmatrix}&space;1&space;&&space;0&space;\\&space;0&space;&&space;1&space;\end{bmatrix}" />

### Examples
X gate:
```py
qc = QuantestPyCircuit(2)
qc.add_gate({
    "name": "x",
    "target_qubit": [0],
    "control_qubit": [],
    "control_value": [],
    "parameter": []
})
qc.draw()
:
0 ─[X]─ 0

1 ───── 1
```
CX gate, conditional on the control qubit being set to 1:
```py
qc = QuantestPyCircuit(2)
qc.add_gate({
    "name": "x",
    "target_qubit": [1],
    "control_qubit": [0],
    "control_value": [1],
    "parameter": []
})
qc.draw()
:
0 ──■── 0
    │
1 ─[X]─ 1
```
CX gate, conditional on the control qubit being set to 0:
```py
qc = QuantestPyCircuit(2)
qc.add_gate({
    "name": "x",
    "target_qubit": [1],
    "control_qubit": [0],
    "control_value": [0],
    "parameter": []
})
qc.draw()
:
0 ──o── 0
    │
1 ─[X]─ 1
```
XX gate:
```py
qc = QuantestPyCircuit(2)
qc.add_gate({
    "name": "x",
    "target_qubit": [0, 1],
    "control_qubit": [],
    "control_value": [],
    "parameter": []
})
qc.draw()
:
0 ─[X]─ 0

1 ─[X]─ 1
```
CCRz gate, conditional on the first control qubit being set to 1 and the second control qubit to 0:
```py
qc = QuantestPyCircuit(3)
qc.add_gate({
    "name": "rz",
    "target_qubit": [2],
    "control_qubit": [0, 1],
    "control_value": [1, 0],
    "parameter": [np.pi/128]
})
qc.draw()
:
0 ───■─── 0
     │
1 ───o─── 1
     │
2 ─[R_z]─ 2
```
