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

Users can always put multi-indices in "target_qubit", "control_qubit" and "control_value" for any gate as long as they are not out of range for circuit size. Controlled gates can be defined by specifying a gate name being performed on a single target qubit (such as "x") and giving a non-empty list to "control_qubit". By providing a non-empty list of 0 and 1 to "control_value", users can define the condition on the control qubit(s) for the gate to be applied on the target qubit(s). By definition, the length of "control_value" must be equal to that of "control_qubit". A non-empty list for "parameter" is allowed only for gates which have parameters such as rotation gates. For better understanding, see examples below.

The following table lists the currently available gates:

name | description | parameter
--- | --- | ---
"x" | X gate | []
"y" | Y gate | []
"z" | Z gate | []
"h" | Hadamard gate | []
"s" | Phase gate | []
"sdg" | Hermitian conjugate of Phase gate | []
"t" | T gate | []
"tdg" | Hermitian conjugate of T gate | []
"rx" | Rx gate | [theta]
"ry" | Ry gate | [theta]
"rz" | Rz gate | [theta]
"u1" | U1 gate | [theta]
"u2" | U2 gate | [phi, lambda]
"u3" | U3 gate | [theta, phi, lambda]
"scalar" | exp(i*theta) * Identity gate | [theta]

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
CX gate, conditional on the control qubit being set to 1.
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
CX gate, conditional on the control qubit being set to 0.
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
