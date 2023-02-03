"""
SAMPLE PROGRAM : L = 8 indexed Majorana fermion operation circuit

REFERENCE : Figure 9 in R. Babbush et al., arXiv:1805.03662
"""


from quantestpy import QuantestPyCircuit, assert_unary_iteration

"""Define a function testing the circuit"""


def test_L8_Majorana_op(circuit):

    assert_unary_iteration(
        circuit=circuit,
        index_reg=[0, 1, 3, 5],
        system_reg=[8, 9, 10, 11, 12, 13, 14, 15],
        ancilla_reg=[2, 4, 6, 7],
        input_to_output={
            "1000": "10000000",
            "1001": "11000000",
            "1010": "11100000",
            "1011": "11110000",
            "1100": "11111000",
            "1101": "11111100",
            "1110": "11111110",
            "1111": "11111111"
        },
        draw_circuit=True
    )


"""Construct the circuit"""
qc = QuantestPyCircuit(16)
qc.add_gate({"name": "x", "target_qubit": [7], "control_qubit": [0],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [2], "control_qubit": [0, 1],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [4], "control_qubit": [2, 3],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [7], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "y", "target_qubit": [8], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "z", "target_qubit": [8], "control_qubit": [7],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [7], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "y", "target_qubit": [9], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "z", "target_qubit": [9], "control_qubit": [7],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [4], "control_qubit": [2],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [7], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "y", "target_qubit": [10], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "z", "target_qubit": [10], "control_qubit": [7],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [7], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "y", "target_qubit": [11], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "z", "target_qubit": [11], "control_qubit": [7],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [4], "control_qubit": [2, 3],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [2], "control_qubit": [0],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [4], "control_qubit": [2, 3],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [7], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "y", "target_qubit": [12], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "z", "target_qubit": [12], "control_qubit": [7],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [7], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "y", "target_qubit": [13], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "z", "target_qubit": [13], "control_qubit": [7],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [4], "control_qubit": [2],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 0]})
qc.add_gate({"name": "x", "target_qubit": [7], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "y", "target_qubit": [14], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "z", "target_qubit": [14], "control_qubit": [7],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [7], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "y", "target_qubit": [15], "control_qubit": [6],
             "control_value": [1]})
qc.add_gate({"name": "x", "target_qubit": [6], "control_qubit": [4, 5],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [4], "control_qubit": [2, 3],
             "control_value": [1, 1]})
qc.add_gate({"name": "x", "target_qubit": [2], "control_qubit": [0, 1],
             "control_value": [1, 1]})


"""Test the circuit.
Get none and confirm that the circuit is constructed as expected.
"""
test_L8_Majorana_op(qc)

"""(Option)
Make a mistake in the circuit intentionally and see how the assert method
works!
"""
qc.add_gate({"name": "x", "target_qubit": [12], "control_qubit": [],
             "control_value": []})
test_L8_Majorana_op(qc)
