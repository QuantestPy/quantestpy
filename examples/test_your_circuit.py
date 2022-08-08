"""
Example showing how to test your own circuit class using TestCircuit class.
"""

import numpy as np

import quantestpy
from quantestpy import TestCircuit


class MyCircuit:
    """My original circuit class
    """

    def __init__(self, n_qubit: int):
        self.gates = []
        self.qubits = [0 for _ in range(n_qubit)]

    def x(self, target: int) -> None:
        """x gate is implemented here"""
        pass

    def h(self, target: int) -> None:
        """Hadmard gate is implemented here"""
        pass

    def cx(self, control: int, target: int) -> None:
        """cx gate is implemented here"""
        pass


def cvt_my_circuit_to_test_circuit(my_circuit: MyCircuit) -> TestCircuit:

    test_circuit = TestCircuit(len(my_circuit.qubits))

    for gate in my_circuit.gates:
        if gate["name"] == "X":
            test_circuit.add_gate(
                {"name": "x",
                 "target_qubit": gate["target"]}
            )
        elif gate["name"] == "H":
            test_circuit.add_gate(
                {"name": "h",
                 "target_qubit": gate["target"]}
            )
        elif gate["name"] == "CNOT":
            test_circuit.add_gate(
                {"name": "cx",
                 "target_qubit": gate["target"],
                 "control_qubit": gate["control"]}
            )
        else:
            raise

    return test_circuit


# build my circuit
my_circuit = MyCircuit(n_qubit=2)
my_circuit.gates.append({"name": "H", "target": 0})
my_circuit.gates.append({"name": "CNOT", "target": 1, "control": 0})

# here I want to test my circuit
# CX (H@I) |q0>@|q1>
test_circuit = cvt_my_circuit_to_test_circuit(my_circuit)
expected_operator = np.array(
    [[1, 0, 1, 0],
     [0, 1, 0, 1],
     [0, 1, 0, -1],
     [1, 0, -1, 0]]
)/np.sqrt(2.) * np.exp(0.4j)

quantestpy.circuit.assert_equal_to_operator(
    expected_operator,
    test_circuit=test_circuit,
    check_including_global_phase=False,
    number_of_decimal_places=5
)

# here I want to test my circuit
# CX (I@H) |q1>@|q0>; Qiskit convention
test_circuit = cvt_my_circuit_to_test_circuit(my_circuit)
expected_operator = np.array(
    [[1, 1, 0, 0],
     [0, 0, 1, -1],
     [0, 0, 1, 1],
     [1, -1, 0, 0]]
)/np.sqrt(2.)

quantestpy.circuit.assert_equal_to_operator(
    expected_operator,
    test_circuit=test_circuit,
    check_including_global_phase=False,
    number_of_decimal_places=5,
    from_right_to_left_for_qubit_ids=True
)
