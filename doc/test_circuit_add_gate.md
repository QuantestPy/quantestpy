# quantestpy.TestCircuit.add_gate

## TestCircuit.add_gate(gate)
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
"id" | Identity gate | [] | $$\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$
"x" | X gate | [] | $$\begin{bmatrix} 0& 1 \\ 1 & 0 \end{bmatrix}$$
"y" | Y gate | [] | $$\begin{bmatrix} 0 & -i \\ i & 0 \end{bmatrix}$$
"z" | Z gate | [] | $$\begin{bmatrix} 1 & 0 \\ 0 & -1 \end{bmatrix}$$
"h" | Hadamard gate | [] | $$\frac{1}{\sqrt{2}}\begin{bmatrix} 1 & 1 \\ 1 & -1 \end{bmatrix}$$
"s" | S gate | [] | $$\begin{bmatrix} 1 & 0 \\ 0 & i \end{bmatrix}$$
"sdg" | Hermitian conjugate of Phase gate | [] | $$\begin{bmatrix} 1 & 0 \\ 0 & -i \end{bmatrix}$$
"t" | T gate | [] | $$\begin{bmatrix} 1 & 0 \\ 0 & e^{i\pi/4} \end{bmatrix}$$
"tdg" | Hermitian conjugate of T gate | [] | $$\begin{bmatrix} 1 & 0 \\ 0 & e^{-i\pi/4} \end{bmatrix}$$
"swap" | Swap gate | [] | $$\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$
"iswap" | iSwap gate | [] | $$\begin{bmatrix} 1 & 0 & 0 & 0 \\ 0 & 0 & i & 0 \\ 0 & i & 0 & 0 \\ 0 & 0 & 0 & 1 \end{bmatrix}$$
"rx" | Rx gate | [$\theta$] | $$\begin{bmatrix} \cos{\frac{\theta}{2}} & -i\sin{\frac{\theta}{2}} \\ -i\sin{\frac{\theta}{2}} & \cos{\frac{\theta}{2}} \end{bmatrix}$$
"ry" | Ry gate | [$\theta$] | $$\begin{bmatrix} \cos{\frac{\theta}{2}} & -\sin{\frac{\theta}{2}} \\ \sin{\frac{\theta}{2}} & \cos{\frac{\theta}{2}} \end{bmatrix}$$
"rz" | Rz gate | [$\theta$] | $$\begin{bmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{bmatrix}$$
"p" | Phase gate | [$\lambda$] | $$\begin{bmatrix} 1 & 0 \\ 0 & e^{i\lambda} \end{bmatrix}$$
"u" | U gate | [$\theta, \phi, \lambda, \gamma$] | $$e^{i\gamma}\begin{bmatrix} \cos{\frac{\theta}{2}} & -e^{i\lambda}\sin{\frac{\theta}{2}} \\ e^{i\phi}\sin{\frac{\theta}{2}} & e^{i(\phi+\lambda)}\cos{\frac{\theta}{2}} \end{bmatrix}$$
"scalar" | exp($i\theta$) * Identity gate | [$\theta$] | $$e^{i\theta}\begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$

### Examples
X gate:
```py
     ┌───┐
q_0: ┤ X ├
     └───┘
q_1: ─────
tc = TestCircuit(2)
tc.add_gate({
    "name": "x",
    "target_qubit": [0]
    "control_qubit": [],
    "control_value": [],
    "parameter": []
})
```
CX gate, conditional on the control qubit being set to 1:
```py
q_0: ──■──
     ┌─┴─┐
q_1: ┤ X ├
     └───┘
tc = TestCircuit(2)
tc.add_gate({
    "name": "x",
    "target_qubit": [1]
    "control_qubit": [0],
    "control_value": [1],
    "parameter": []
})
```
CX gate, conditional on the control qubit being set to 0:
```py
q_0: ──O──
     ┌─┴─┐
q_1: ┤ X ├
     └───┘
tc = TestCircuit(2)
tc.add_gate({
    "name": "x",
    "target_qubit": [1]
    "control_qubit": [0],
    "control_value": [0],
    "parameter": []
})
```
XX gate:
```py
     ┌───┐
q_0: ┤ X ├
     ├───┤
q_1: ┤ X ├
     └───┘
tc = TestCircuit(2)
tc.add_gate({
    "name": "x",
    "target_qubit": [0, 1]
    "control_qubit": [],
    "control_value": [],
    "parameter": []
})
```
CCRz gate, conditional on the first control qubit being set to 1 and the second control qubit to 0:
```py
q_0: ──────■──────
           │
q_1: ──────O──────
     ┌─────┴─────┐
q_2: ┤ Rz(π/128) ├
     └───────────┘
tc = TestCircuit(3)
tc.add_gate({
    "name": "rz",
    "target_qubit": [2]
    "control_qubit": [0, 1],
    "control_value": [1, 0],
    "parameter": [np.pi/128]
})
```
The circuit diagrams above are drawn with the help of `qiskit`.
