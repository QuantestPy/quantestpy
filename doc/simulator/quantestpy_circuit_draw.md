# quantestpy.QuantestPyCircuit.draw

## QuantestPyCircuit.draw()
Draws the circuit.

### Examples
```py
In [1]: from quantestpy import QuantestPyCircuit

In [2]: qc = QuantestPyCircuit(3)
   ...: qc.add_gate({"name": "x", "control_qubit": [], "target_qubit": [0], "control_value": []})
   ...: qc.add_gate({"name": "z", "control_qubit": [0], "target_qubit": [2], "control_value": [1]})

In [3]: qc.draw()
Out[3]:
0 ─[X]─■── 0
       │
1 ─────┼── 1
       │
2 ────[Z]─ 2
```
