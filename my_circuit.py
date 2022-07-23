import numpy as np
import qiskit
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

    def state_vector(self,) -> np.ndarray:
        for gate in self.gates:
            if gate["name"] == "x":
                self.x(gate["target"])
            elif gate["name"] == "cx":
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
                state_vec = self.tensor_prod_vec(state_vec, vec)

        return state_vec

    @staticmethod
    def tensor_prod_vec(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        tmp = np.array([])
        for i in a:
            c = i * b
            tmp = np.append(tmp, c)
        return tmp

    @staticmethod
    def tensor_prod_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        m = a.shape[0]
        n = a.shape[1]
        for i in range(m):
            for j in range(n):
                c = a[i, j] * b
                if j == 0:
                    column = c
                else:
                    column = np.append(column, c, axis=1)

            if i == 0:
                row = column
            else:
                row = np.append(row, column, axis=0)

        return row

    def cvt_my_circuit_to_qasm(self,
                               filename: str = "./my_circuit.qasm") -> str:

        s = "OPENQASM 2.0;\n"
        s += 'include "qelib1.inc";\n'
        s += f"qreg q[{len(self.qubits)}];\n"

        for gate in self.gates:
            if gate["name"] == "x":
                s += f'x q[{gate["target"]}];\n'
            elif gate["name"] == "cx":
                s += f'cx q[{gate["control"]}],q[{gate["target"]}];\n'
            else:
                raise

        with open(filename, mode="w") as f:
            f.write(s)

        return s

    def cvt_my_circuit_to_qiskit_circuit(self,) -> qiskit.QuantumCircuit:

        qiskit_circ = qiskit.QuantumCircuit(len(self.qubits))
        for gate in self.gates:
            if gate["name"] == "x":
                qiskit_circ.x(gate["target"])
            elif gate["name"] == "cx":
                qiskit_circ.cx(gate["control"], gate["target"])
            else:
                raise

        return qiskit_circ
