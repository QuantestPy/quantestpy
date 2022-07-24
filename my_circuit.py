import numpy as np
import qiskit
from quantestpy import TestCircuit
# my original circuit class


class MyCircuit:
    def __init__(self, n_qubit: int):
        self.gates = []
        # Example:
        # self.gates = [
        #    {"name": "x", "target": 1},
        #    {"name": "cx", "target": 2, "control": 1},
        #    {"name": "x", "target": 2}
        # ]
        self.qubits = [0 for _ in range(n_qubit)]

    def x(self, target: int) -> None:
        if self.qubits[target] == 0:
            self.qubits[target] = 1
        elif self.qubits[target] == 1:
            self.qubits[target] = 0
        else:
            raise

    def cx(self, control: int, target: int) -> None:
        if self.qubits[control] == 1:
            self.x(target)

    def get_state_vector(self,) -> np.ndarray:
        for gate in self.gates:
            if gate["name"] == "X":
                self.x(gate["target"])
            elif gate["name"] == "CNOT":
                self.cx(gate["control"], gate["target"])
            else:
                raise

        self.vecs = []
        for qubit in self.qubits:
            if qubit == 0:
                self.vecs.append(np.array([1, 0]))
            elif qubit == 1:
                self.vecs.append(np.array([0, 1]))
            else:
                raise

        for i, vec in enumerate(self.vecs):
            if i == 0:
                state_vec = vec
            else:
                state_vec = self.create_tensor_prod_vec(state_vec, vec)

        return state_vec

    @staticmethod
    def create_tensor_prod_vec(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        tmp = np.array([])
        for i in a:
            c = i * b
            tmp = np.append(tmp, c)
        return tmp

    def cvt_my_circuit_to_qasm(self,
                               filename: str = "./my_circuit.qasm") -> str:

        s = "OPENQASM 2.0;\n"
        s += 'include "qelib1.inc";\n'
        s += f"qreg q[{len(self.qubits)}];\n"

        for gate in self.gates:
            if gate["name"] == "X":
                s += f'x q[{gate["target"]}];\n'
            elif gate["name"] == "CNOT":
                s += f'cx q[{gate["control"]}],q[{gate["target"]}];\n'
            else:
                raise

        with open(filename, mode="w") as f:
            f.write(s)

        return s

    def cvt_my_circuit_to_qiskit_circuit(self,) -> qiskit.QuantumCircuit:
        """Note that reverse in qubit is done.
        This is needed to reproduce the same state vector with qiskit.
        """

        qiskit_circ = qiskit.QuantumCircuit(len(self.qubits))
        for gate in self.gates:
            if gate["name"] == "X":
                qiskit_circ.x(len(self.qubits)-1-gate["target"])
            elif gate["name"] == "CNOT":
                qiskit_circ.cx(len(self.qubits)-1-gate["control"],
                               len(self.qubits)-1-gate["target"])
            else:
                raise

        return qiskit_circ

    def cvt_my_circuit_to_test_circuit(self,) -> TestCircuit:

        test_circuit = TestCircuit(len(self.qubits))

        for gate in self.gates:
            if gate["name"] == "X":
                test_circuit.add_gate(
                    {"name": "x",
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


if __name__ == "__main__":
    """Example showing how to use MyCircuit class."""

    # construct circuit
    my_circ = MyCircuit(n_qubit=2)
    my_circ.gates.append({"name": "X", "target": 0})
    my_circ.gates.append({"name": "CNOT", "target": 1, "control": 0})
    state_vector = my_circ.get_state_vector()

    # convert to qasm
    qasm = my_circ.cvt_my_circuit_to_qasm()

    # convert to qiskit circuit
    qiskit_circ = my_circ.cvt_my_circuit_to_qiskit_circuit()

    # convert to test circuit
    test_circ = my_circ.cvt_my_circuit_to_test_circuit()
