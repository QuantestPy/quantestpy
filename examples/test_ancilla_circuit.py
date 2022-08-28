"""
Example showing how to check ancilla qubits to be zero in your own circuit.
"""
from quantestpy import TestCircuit, circuit


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
                 "target_qubit": [gate["target"]],
                 "control_qubit": [],
                 "control_value": [],
                 "parameter": []}
            )
        elif gate["name"] == "H":
            test_circuit.add_gate(
                {"name": "h",
                 "target_qubit": [gate["target"]],
                 "control_qubit": [],
                 "control_value": [],
                 "parameter": []}
            )
        elif gate["name"] == "CNOT":
            test_circuit.add_gate(
                {"name": "cx",
                 "target_qubit": [gate["target"]],
                 "control_qubit": [gate["control"]],
                 "control_value": [1],
                 "parameter": []}
            )
        else:
            raise

    return test_circuit


# build my circuit no.1
my_circuit = MyCircuit(n_qubit=2)
my_circuit.gates.append({"name": "X", "target": 0})
my_circuit.gates.append({"name": "CNOT", "control": 0, "target": 1})

my_circuit.gates.append({"name": "CNOT", "control": 0, "target": 1})
my_circuit.gates.append({"name": "X", "target": 0})

# here I want to test my circuit
test_circuit = cvt_my_circuit_to_test_circuit(my_circuit)

circuit.assert_is_zero(
    test_circuit=test_circuit,
    qubits=[0, 1],
    number_of_decimal_places=5
)


# build my circuit no.2
my_circuit = MyCircuit(n_qubit=2)
my_circuit.gates.append({"name": "X", "target": 0})
my_circuit.gates.append({"name": "CNOT", "control": 0, "target": 1})

# here I want to test my circuit
test_circuit = cvt_my_circuit_to_test_circuit(my_circuit)

circuit.assert_is_zero(
    test_circuit=test_circuit,
    qubits=[0, 1],
    number_of_decimal_places=5
)


# build my circuit no.3
my_circuit = MyCircuit(n_qubit=2)
my_circuit.gates.append({"name": "H", "target": 0})
my_circuit.gates.append({"name": "CNOT", "control": 0, "target": 1})

# here I want to test my circuit
test_circuit = cvt_my_circuit_to_test_circuit(my_circuit)

circuit.assert_is_zero(
    test_circuit=test_circuit,
    qubits=[0, 1],
    number_of_decimal_places=5
)
