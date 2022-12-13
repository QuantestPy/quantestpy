# quantestpy.assert_get_ctrl_val

## assert_get_ctrl_val(circuit, ctrl_reg, ancilla_reg=[], check_ancilla_is_uncomputed=False, print_out_result=True)

Returns the values of control qubits for all gates in the circuit.

### Parameters

#### circuit: quantestpy.PauliCircuit
The circuit to check. [quantestpy.PauliCircuit](./pauli_circuit.md) is a circuit class developed in this project.

#### ctrl_reg : list
A list of qubit ids. The output of this method contains the result from all possible initial states for these qubits.

#### ancilla_reg : list, optional
A list of qubit ids. These qubits are assumed to be 0 in the initial states.

#### check_ancilla_is_uncomputed : bool, optional
If True, raises a QuantestPyAssertionError if the qubits in `ancilla_reg` are not uncomputed to 0 at the end.

#### print_out_result : bool, optional
If True, prints out the result in the stdout.

### Returns

#### output : dict

The key is the control qubit id in the circuit and the value is another dictionary, whose key is the initial state for the qubits in `ctrl_reg` and value is a list of the values of the control qubit.

### Examples
The following circuit is an L=6 unary iteration circuit, which is a variant of the circuit in Figure 7 in [arXiv:1805.03662](https://arxiv.org/abs/1805.03662):
```py
0   |0> ──■───────────────────────────────────────────────────────■───────────────────────■──
          │                                                       │                       │
1   |0> ──o───────────────────────────────────────────────────────┼───────────────────────■──
          │                                                       │                       │
2   |0> ─[X]──■───────────────────────■───────────────────────■──[X]──■───────■───────■──[X]─
              │                       │                       │       │       │       │
3   |0> ──────o───────────────────────┼───────────────────────■───────┼───────┼───────┼──────
              │                       │                       │       │       │       │
4   |0> ─────[X]──■───────■───────■──[X]──■───────■───────■──[X]──────┼───────┼───────┼──────
                  │       │       │       │       │       │           │       │       │
5   |0> ──────────o───────┼───────■───────o───────┼───────■───────────o───────┼───────■──────
                  │       │       │       │       │       │           │       │       │
6   |0> ─────────[X]──■──[X]──■──[X]─────[X]──■──[X]──■──[X]─────────[X]──■──[X]──■──[X]─────
                      │       │               │       │                   │       │
7   |0> ─────────────[Y]──────┼───────────────┼───────┼───────────────────┼───────┼──────────
                              │               │       │                   │       │
8   |0> ─────────────────────[Y]──────────────┼───────┼───────────────────┼───────┼──────────
                                              │       │                   │       │
9   |0> ─────────────────────────────────────[Y]──────┼───────────────────┼───────┼──────────
                                                      │                   │       │
10  |0> ─────────────────────────────────────────────[Y]──────────────────┼───────┼──────────
                                                                          │       │
11  |0> ─────────────────────────────────────────────────────────────────[Y]──────┼──────────
                                                                                  │
12  |0> ─────────────────────────────────────────────────────────────────────────[Y]─────────

from quantestpy import PauliCircuit, assert_get_ctrl_val

pc = PauliCircuit(13)
pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2], "control_value": [1, 0]})
pc.add_gate({"name": "x", "control_qubit": [2, 3], "target_qubit": [4], "control_value": [1, 0]})
pc.add_gate({"name": "x", "control_qubit": [4, 5], "target_qubit": [6], "control_value": [1, 0]})
pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [7], "control_value": [1]})
pc.add_gate({"name": "x", "control_qubit": [4], "target_qubit": [6], "control_value": [1]})
pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [8], "control_value": [1]})
pc.add_gate({"name": "x", "control_qubit": [4, 5], "target_qubit": [6], "control_value": [1, 1]})
pc.add_gate({"name": "x", "control_qubit": [2], "target_qubit": [4], "control_value": [1]})
pc.add_gate({"name": "x", "control_qubit": [4, 5], "target_qubit": [6], "control_value": [1, 0]})
pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [9], "control_value": [1]})
pc.add_gate({"name": "x", "control_qubit": [4], "target_qubit": [6], "control_value": [1]})
pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [10], "control_value": [1]})
pc.add_gate({"name": "x", "control_qubit": [4, 5], "target_qubit": [6], "control_value": [1, 1]})
pc.add_gate({"name": "x", "control_qubit": [2, 3], "target_qubit": [4], "control_value": [1, 1]})
pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [2], "control_value": [1]})
pc.add_gate({"name": "x", "control_qubit": [2, 5], "target_qubit": [6], "control_value": [1, 0]})
pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [11], "control_value": [1]})
pc.add_gate({"name": "x", "control_qubit": [2], "target_qubit": [6], "control_value": [1]})
pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [12], "control_value": [1]})
pc.add_gate({"name": "x", "control_qubit": [2, 5], "target_qubit": [6], "control_value": [1, 1]})
pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2], "control_value": [1, 1]})

output = assert_get_ctrl_val(
    circuit=pc,
    ctrl_reg=[0, 1, 3, 5],
    ancilla_reg=[2, 4, 6],
    check_ancilla_is_uncomputed=True,
    print_out_result=False
)
```
Since the values of the control qubit `6` are of great concern to the developer, she/he would get
```py
output[6]
{'0000': [0, 0, 0, 0, 0, 0],
 '0001': [0, 0, 0, 0, 0, 0],
 '0010': [0, 0, 0, 0, 0, 0],
 '0011': [0, 0, 0, 0, 0, 0],
 '0100': [0, 0, 0, 0, 0, 0],
 '0101': [0, 0, 0, 0, 0, 0],
 '0110': [0, 0, 0, 0, 0, 0],
 '0111': [0, 0, 0, 0, 0, 0],
 '1000': [1, 0, 0, 0, 0, 0],
 '1001': [0, 1, 0, 0, 0, 0],
 '1010': [0, 0, 1, 0, 0, 0],
 '1011': [0, 0, 0, 1, 0, 0],
 '1100': [0, 0, 0, 0, 1, 0],
 '1101': [0, 0, 0, 0, 0, 1],
 '1110': [0, 0, 0, 0, 1, 0],
 '1111': [0, 0, 0, 0, 0, 1]}
 ```
