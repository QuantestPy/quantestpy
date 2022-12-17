# quantestpy.PauliCircuit.draw

## PauliCircuit.draw()
Draws the circuit.

### Examples
```py
In [1]: from quantestpy import PauliCircuit

In [2]: pc = PauliCircuit(13)
   ...: pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2], "control_value": [1, 0]})
   ...: pc.add_gate({"name": "x", "control_qubit": [2, 3], "target_qubit": [4], "control_value": [1, 0]})
   ...: pc.add_gate({"name": "x", "control_qubit": [4, 5], "target_qubit": [6], "control_value": [1, 0]})
   ...: pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [7], "control_value": [1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [4], "target_qubit": [6], "control_value": [1]})
   ...: pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [8], "control_value": [1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [4, 5], "target_qubit": [6], "control_value": [1, 1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [2], "target_qubit": [4], "control_value": [1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [4, 5], "target_qubit": [6], "control_value": [1, 0]})
   ...: pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [9], "control_value": [1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [4], "target_qubit": [6], "control_value": [1]})
   ...: pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [10], "control_value": [1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [4, 5], "target_qubit": [6], "control_value": [1, 1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [2, 3], "target_qubit": [4], "control_value": [1, 1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [2], "control_value": [1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [2, 5], "target_qubit": [6], "control_value": [1, 0]})
   ...: pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [11], "control_value": [1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [2], "target_qubit": [6], "control_value": [1]})
   ...: pc.add_gate({"name": "y", "control_qubit": [6], "target_qubit": [12], "control_value": [1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [2, 5], "target_qubit": [6], "control_value": [1, 1]})
   ...: pc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2], "control_value": [1, 1]})

In [3]: pc.draw()
Out[3]:
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

```
