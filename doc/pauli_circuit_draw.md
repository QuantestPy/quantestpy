# quantestpy.PauliCircuit.draw

## PauliCircuit.draw()
Draws the circuit.

### Examples
```py
In [1]: from quantestpy import PauliCircuit

In [2]: pc = PauliCircuit(3)
   ...: pc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [0], "control_value": []})
   ...: pc.add_gate({"name": "z", "control_qubit": [0], "target_qubit": [2], "control_value": [1]})

In [3]: pc.draw()
Out[3]:
0  |0> ─[X]──■──
             │
1  |0> ──────┼──
             │
2  |0> ─────[Z]─

In [4]:
```
