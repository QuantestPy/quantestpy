"""
SAMPLE PROGRAM : L = 11 unary iteration circuit

REFERENCE : Figure 7 in R. Babbush et al., arXiv:1805.03662
"""


from quantestpy import QuantestPyCircuit, assert_unary_iteration

"""Define a function testing the circuit"""


def test_L11_unary_iteration(circuit):

    assert_unary_iteration(
        circuit=circuit,
        index_reg=[0, 1, 3, 5, 7],
        system_reg=[9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        ancilla_reg=[2, 4, 6, 8],
        input_to_output={
            "10000": "10000000000",
            "10001": "01000000000",
            "10010": "00100000000",
            "10011": "00010000000",
            "10100": "00001000000",
            "10101": "00000100000",
            "10110": "00000010000",
            "10111": "00000001000",
            "11000": "00000000100",
            "11001": "00000000010",
            "11010": "00000000001"
        },
        draw_circuit=True
    )


"""Construct the circuit"""
qc = QuantestPyCircuit(20)
qc.add_gate({"name": "x", "target_qubit": [2], "control_qubit": [0, 1],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [4], "control_qubit": [2, 3],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6, 7],
             "control_value": [1, 0]})
# Z_0
qc.add_gate({"name": "z", "target_qubit": [9], "control_qubit": [8],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6],
             "control_value": [1]})
# Z_1
qc.add_gate({"name": "z", "target_qubit": [10], "control_qubit": [8],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6, 7],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6, 7],
             "control_value": [1, 0]})
# Z_2
qc.add_gate({"name": "z", "target_qubit": [11], "control_qubit": [8],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6],
             "control_value": [1]})
# Z_3
qc.add_gate({"name": "z", "target_qubit": [12], "control_qubit": [8],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6, 7],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [4], "control_qubit": [2],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6, 7],
             "control_value": [1, 0]})
# Z_4
qc.add_gate({"name": "z", "target_qubit": [13], "control_qubit": [8],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6],
             "control_value": [1]})
# Z_5
qc.add_gate({"name": "z", "target_qubit": [14], "control_qubit": [8],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6, 7],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6, 7],
             "control_value": [1, 0]})
# Z_6
qc.add_gate({"name": "z", "target_qubit": [15], "control_qubit": [8],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6],
             "control_value": [1]})
# Z_7
qc.add_gate({"name": "z", "target_qubit": [16], "control_qubit": [8],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6, 7],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [4], "control_qubit": [2, 3],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [2], "control_qubit": [0],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [2, 5],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6, 7],
             "control_value": [1, 0]})
# Z_8
qc.add_gate({"name": "z", "target_qubit": [17], "control_qubit": [8],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6],
             "control_value": [1]})
# Z_9
qc.add_gate({"name": "z", "target_qubit": [18], "control_qubit": [8],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [8], "control_qubit": [6, 7],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [2],
             "control_value": [1]})
# Z_10
qc.add_gate({"name": "z", "target_qubit": [19], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [2, 5],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [2], "control_qubit": [0, 1],
             "control_value": [1, 1]})

"""Test the circuit.
Get none and confirm that the circuit is constructed as expected.
"""
test_L11_unary_iteration(circuit=qc)

"""(Option)
Make a mistake in the circuit intentionally and see how the assert method
works!
"""
qc.add_gate({"name": "x", "target_qubit": [18], "control_qubit": [],
             "control_value": []})
test_L11_unary_iteration(circuit=qc)
