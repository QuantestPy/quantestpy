"""
SAMPLE PROGRAM : 5-bit adder

REFERENCE : Figure 1 in C. Gidney, arXiv:1709.06648
"""


from quantestpy import (QuantestPyCircuit,
                        assert_circuit_equivalent_to_output_qubit_state)

"""Define a function testing the circuit"""


def test_5_bit_adder(circuit):
    """a + b = c"""

    for decimal_a in range(2**5):
        for decimal_b in range(2**5):
            decimal_c = decimal_a + decimal_b
            if decimal_c > 31:
                continue
            bitstring_a = ("0" * 5 + bin(decimal_a)[2:])[-5:]
            bitstring_b = ("0" * 5 + bin(decimal_b)[2:])[-5:]
            bitstring_c = ("0" * 5 + bin(decimal_c)[2:])[-5:]

            assert_circuit_equivalent_to_output_qubit_state(
                circuit=circuit,
                # input_reg = reg. for a + reg. for b
                input_reg=[12, 9, 6, 3, 0, 13, 10, 7, 4, 1],
                output_reg=[13, 10, 7, 4, 1],  # output_reg = reg. for c
                input_to_output={
                    bitstring_a + bitstring_b: bitstring_c
                },  # input (= a + b) : output (= c)
                draw_circuit=True
            )


"""Construct the circuit"""
qc = QuantestPyCircuit(14)
qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
            "control_value": [1, 1]})
qc.add_gate({"name": "x", "control_qubit": [2], "target_qubit": [3, 4],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [3, 4], "target_qubit": [5],
            "control_value": [1, 1]})
qc.add_gate({"name": "x", "control_qubit": [2], "target_qubit": [5],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [5], "target_qubit": [6, 7],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [6, 7], "target_qubit": [8],
            "control_value": [1, 1]})
qc.add_gate({"name": "x", "control_qubit": [5], "target_qubit": [8],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [8], "target_qubit": [9, 10],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [9, 10], "target_qubit": [11],
            "control_value": [1, 1]})
qc.add_gate({"name": "x", "control_qubit": [8], "target_qubit": [11],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [11], "target_qubit": [13],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [8], "target_qubit": [11],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [9, 10], "target_qubit": [11],
            "control_value": [1, 1]})
qc.add_gate({"name": "x", "control_qubit": [8], "target_qubit": [9],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [5], "target_qubit": [8],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [6, 7], "target_qubit": [8],
            "control_value": [1, 1]})
qc.add_gate({"name": "x", "control_qubit": [5], "target_qubit": [6],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [2], "target_qubit": [5],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [3, 4], "target_qubit": [5],
            "control_value": [1, 1]})
qc.add_gate({"name": "x", "control_qubit": [2], "target_qubit": [3],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [0, 1], "target_qubit": [2],
            "control_value": [1, 1]})
qc.add_gate({"name": "x", "control_qubit": [0], "target_qubit": [1],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [3], "target_qubit": [4],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [6], "target_qubit": [7],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [9], "target_qubit": [10],
            "control_value": [1]})
qc.add_gate({"name": "x", "control_qubit": [12], "target_qubit": [13],
            "control_value": [1]})

"""Test the circuit.
Get none and confirm that the circuit is constructed as expected.
"""
test_5_bit_adder(circuit=qc)

"""(Option)
Make a mistake in the circuit intentionally and see how the assert method
works!
"""
qc.add_gate({"name": "x", "control_qubit": [12], "target_qubit": [13],
            "control_value": [1]})
test_5_bit_adder(circuit=qc)
